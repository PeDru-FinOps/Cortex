import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from cortex_notes.agent import CortexAgent, build_llm_prompt, tokenize, vector_store_result_to_context
from cortex_notes.repository import NoteRepository


class AgentTest(unittest.TestCase):
    def test_tokenize_removes_common_words_and_accents(self):
        terms = tokenize("A automação de custos também depende de decisões.")

        self.assertIn("automacao", terms)
        self.assertIn("custos", terms)
        self.assertNotIn("tambem", terms)

    def test_agent_retrieves_relevant_context(self):
        with tempfile.TemporaryDirectory() as folder:
            repository = NoteRepository(folder)
            repository.write_note("Finops/Tags.md", "# Tags\n\nAlocacao de custos por tags.")
            repository.write_note("Teologia/Batismo.md", "# Batismo\n\nEstudo doutrinario.")

            result = CortexAgent(repository).run(query="custos tags")

            self.assertEqual(result["context"][0]["path"], "Finops/Tags.md")
            self.assertIn("custos", result["synthesis"])

    def test_agent_suggests_implicit_relation_for_similar_notes(self):
        with tempfile.TemporaryDirectory() as folder:
            repository = NoteRepository(folder)
            repository.write_note("a.md", "# Kubernetes\n\nReduzir custos de cluster kubernetes.")
            repository.write_note("b.md", "# GKE\n\nCluster kubernetes com custos e alocacao.")
            repository.write_note("c.md", "# Outro\n\nAssunto distante.")

            result = CortexAgent(repository).run(query="kubernetes custos")
            pairs = {(item["source"], item["target"]) for item in result["implicit_relations"]}

            self.assertIn(("a.md", "b.md"), pairs)

    def test_chat_falls_back_without_openai_key(self):
        with tempfile.TemporaryDirectory() as folder:
            repository = NoteRepository(folder)
            repository.write_note("a.md", "# FinOps\n\nTags ajudam na alocacao de custos.")

            with patch.dict("os.environ", {"OPENAI_API_KEY": ""}):
                result = CortexAgent(repository).chat("como usar tags?")

            self.assertFalse(result["llm"]["enabled"])
            self.assertIn("answer", result)

    def test_build_llm_prompt_includes_context_sources(self):
        prompt = build_llm_prompt(
            "pergunta",
            {
                "focus": {"path": "a.md"},
                "context": [{"path": "a.md", "score": 0.9, "excerpt": "Trecho"}],
                "patterns": [],
                "implicit_relations": [],
            },
        )

        self.assertIn("Fonte: a.md", prompt)
        self.assertIn("Pergunta do usuario", prompt)

    def test_openai_vector_store_mode_falls_back_without_key(self):
        with tempfile.TemporaryDirectory() as folder:
            repository = NoteRepository(folder)
            repository.write_note("a.md", "# Tags\n\nAlocacao de custos por tags.")

            with patch.dict(
                "os.environ",
                {"CORTEX_VECTOR_STORE": "openai", "OPENAI_VECTOR_STORE_ID": "vs_test", "OPENAI_API_KEY": ""},
            ):
                context = CortexAgent(repository).search("custos tags")

            self.assertEqual(context[0]["source"], "local-tfidf")

    def test_vector_store_result_is_converted_to_context(self):
        class TextPart:
            text = "Conteudo relevante do vector store."

        class Result:
            filename = "Notas.md"
            file_id = "file_test"
            score = 0.91
            content = [TextPart()]

        context = vector_store_result_to_context(Result())

        self.assertEqual(context["source"], "openai-vector-store")
        self.assertEqual(context["path"], "Notas.md")

    def test_recommend_connections_adds_metadata(self):
        with tempfile.TemporaryDirectory() as folder:
            repository = NoteRepository(folder)
            repository.write_note("a.md", "# Kubernetes\n\nReduzir custos de cluster kubernetes.")
            repository.write_note("b.md", "# GKE\n\nCluster kubernetes com custos e alocacao.")

            result = CortexAgent(repository).recommend_connections()

            self.assertTrue(result["recommendations"])
            self.assertIn("metadata", result["recommendations"][0])

    def test_recommend_connections_filters_rejected_pairs(self):
        with tempfile.TemporaryDirectory() as folder:
            repository = NoteRepository(folder)
            repository.write_note("a.md", "# Kubernetes\n\nReduzir custos de cluster kubernetes.")
            repository.write_note("b.md", "# GKE\n\nCluster kubernetes com custos e alocacao.")

            result = CortexAgent(repository).recommend_connections(
                rejected_pairs={("a.md", "b.md")}
            )

            self.assertEqual(result["recommendations"], [])

    def test_write_content_uses_linkedin_skill_when_available(self):
        with tempfile.TemporaryDirectory() as folder:
            repository = NoteRepository(folder)
            repository.write_note("IA/Skills/linkedin_posts_skill.md", "# LinkedIn Skill")
            repository.write_note("base.md", "# FinOps\n\nTags e alocacao de custos.")

            with patch.dict("os.environ", {"OPENAI_API_KEY": "", "CORTEX_PRIVATE_SKILLS_DIR": f"{folder}/private-empty"}):
                result = CortexAgent(repository).write_content("linkedin", "tags")

            self.assertEqual(result["kind"], "linkedin")
            self.assertEqual(result["skill"], "IA/Skills/linkedin_posts_skill.md")
            self.assertIn("content", result)

    def test_write_content_loads_private_reviewer_skill_when_available(self):
        with tempfile.TemporaryDirectory() as folder:
            repository = NoteRepository(folder)
            repository.write_note("IA/Skills/linkedin_posts_skill.md", "# LinkedIn Skill")
            repository.write_note("base.md", "# FinOps\n\nTags e alocacao de custos.")
            private_dir = f"{folder}/private"
            private_skill = Path(private_dir) / "revisor_pedro" / "SKILL.md"
            private_skill.parent.mkdir(parents=True)
            private_skill.write_text("# Skill privada", encoding="utf-8")

            with patch.dict("os.environ", {"OPENAI_API_KEY": "", "CORTEX_PRIVATE_SKILLS_DIR": private_dir}):
                result = CortexAgent(repository).write_content("linkedin", "tags")

            self.assertIn("IA/Skills/linkedin_posts_skill.md", result["skill"])
            self.assertIn("revisor_pedro", result["skill"])

    def test_private_security_skills_are_loaded_for_writing(self):
        with tempfile.TemporaryDirectory() as folder:
            repository = NoteRepository(folder)
            repository.write_note("IA/Skills/newsletter_skill.md", "# Newsletter Skill")
            repository.write_note("base.md", "# FinOps\n\nTags e alocacao de custos.")
            private_dir = f"{folder}/private"
            for name in ["agente_security", "security_reviwer"]:
                private_skill = Path(private_dir) / name / "SKILL.md"
                private_skill.parent.mkdir(parents=True, exist_ok=True)
                private_skill.write_text(f"# {name}", encoding="utf-8")

            with patch.dict("os.environ", {"OPENAI_API_KEY": "", "CORTEX_PRIVATE_SKILLS_DIR": private_dir}):
                result = CortexAgent(repository).write_content("article", "tags")

            self.assertIn("agente_security", result["skill"])
            self.assertIn("security_reviwer", result["skill"])


if __name__ == "__main__":
    unittest.main()
