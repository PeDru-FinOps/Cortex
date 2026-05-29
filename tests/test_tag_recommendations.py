import tempfile
import unittest

from app import recommend_tags_for_note
from cortex_notes.repository import NoteRepository


class TagRecommendationTest(unittest.TestCase):
    def test_does_not_suggest_unrelated_existing_tags(self):
        with tempfile.TemporaryDirectory() as folder:
            repository = NoteRepository(folder)
            repository.write_note(
                "Artigos/relacionamento.md",
                "# Relacionamento cristao\n\nAlianca, casamento, maturidade, discernimento e proposito diante de Deus.",
            )
            repository.write_note("Cloud/oci.md", "# OCI\n\nOracle cloud compute tenancy network #oci")
            repository.write_note("IA/ia.md", "# IA\n\nAgentes modelos prompts embeddings #ia")

            tags = recommend_tags_for_note(repository, "Artigos/relacionamento.md")

            self.assertNotIn("oci", {item["tag"] for item in tags})
            self.assertNotIn("ia", {item["tag"] for item in tags})

    def test_suggests_tags_from_related_notes(self):
        with tempfile.TemporaryDirectory() as folder:
            repository = NoteRepository(folder)
            repository.write_note(
                "Artigos/relacionamento.md",
                "# Relacionamento cristao\n\nAlianca casamento maturidade discernimento proposito diante de Deus.",
            )
            repository.write_note(
                "Teologia/relacionamento.md",
                "# Relacionamento com proposito\n\nAlianca casamento maturidade discernimento proposito diante de Deus. #teologia #relacionamentos",
            )

            tags = recommend_tags_for_note(repository, "Artigos/relacionamento.md")

            self.assertIn("teologia", {item["tag"] for item in tags})
            self.assertIn("relacionamentos", {item["tag"] for item in tags})


if __name__ == "__main__":
    unittest.main()
