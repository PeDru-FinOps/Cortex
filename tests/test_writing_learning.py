import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from cortex_notes.writing_learning import load_private_reviewer_skill, record_writing_learning


class WritingLearningTest(unittest.TestCase):
    def test_records_learning_in_private_reviewer_skill(self):
        with tempfile.TemporaryDirectory() as folder:
            with patch.dict("os.environ", {"CORTEX_PRIVATE_SKILLS_DIR": folder}):
                result = record_writing_learning(
                    original="Texto muito generico.\n\nConclusao longa demais.",
                    edited="Texto direto, com minha voz.\n\nConclusao objetiva.",
                    kind="article",
                    title="FinOps",
                )
                skill = load_private_reviewer_skill()

            self.assertTrue(result["recorded"])
            self.assertTrue(Path(result["path"]).match("*/revisor_pedro/SKILL.md"))
            self.assertIn("Skill: revisor_pedro", skill["content"])
            self.assertIn("nao uma preferencia permanente contra o tema", skill["content"])
            self.assertIn("nao transformar assuntos removidos em temas proibidos", skill["content"])
            self.assertIn("Texto muito generico.", skill["content"])
            self.assertIn("Texto direto, com minha voz.", skill["content"])

    def test_skips_when_text_was_not_edited(self):
        with tempfile.TemporaryDirectory() as folder:
            with patch.dict("os.environ", {"CORTEX_PRIVATE_SKILLS_DIR": folder}):
                result = record_writing_learning("Mesmo texto", "Mesmo texto")

            self.assertFalse(result["recorded"])
            self.assertFalse(Path(folder, "revisor_pedro", "SKILL.md").exists())


if __name__ == "__main__":
    unittest.main()
