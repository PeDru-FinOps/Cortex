import tempfile
import unittest
from io import BytesIO

from cortex_notes.repository import NoteRepository, RepositoryError


class RepositoryTest(unittest.TestCase):
    def test_write_and_read_note(self):
        with tempfile.TemporaryDirectory() as folder:
            repository = NoteRepository(folder)

            repository.write_note("area/minha-nota", "# Oi")

            note = repository.read_note("area/minha-nota.md")
            self.assertEqual(note["path"], "area/minha-nota.md")
            self.assertEqual(note["content"], "# Oi")

    def test_rejects_path_traversal(self):
        with tempfile.TemporaryDirectory() as folder:
            repository = NoteRepository(folder)

            with self.assertRaises(RepositoryError):
                repository.write_note("../fora.md", "nao")

    def test_create_folder(self):
        with tempfile.TemporaryDirectory() as folder:
            repository = NoteRepository(folder)

            created = repository.create_folder("area/projetos")

            self.assertEqual(created, "area/projetos")

    def test_import_note_stream_preserves_subfolders(self):
        with tempfile.TemporaryDirectory() as folder:
            repository = NoteRepository(folder)

            imported = repository.import_note_stream(
                "base/sub/nota.md",
                BytesIO("# Importada".encode("utf-8")),
            )

            self.assertEqual(imported, "base/sub/nota.md")
            self.assertEqual(repository.read_note(imported)["content"], "# Importada")

    def test_import_rejects_non_markdown_files(self):
        with tempfile.TemporaryDirectory() as folder:
            repository = NoteRepository(folder)

            with self.assertRaises(RepositoryError):
                repository.import_note_stream("arquivo.txt", BytesIO(b"texto"))

    def test_move_note_to_existing_folder(self):
        with tempfile.TemporaryDirectory() as folder:
            repository = NoteRepository(folder)
            repository.write_note("origem/nota.md", "# Nota")
            repository.create_folder("destino")

            moved = repository.move_note("origem/nota.md", "destino")

            self.assertEqual(moved, "destino/nota.md")
            self.assertEqual(repository.read_note(moved)["content"], "# Nota")

    def test_delete_note(self):
        with tempfile.TemporaryDirectory() as folder:
            repository = NoteRepository(folder)
            repository.write_note("nota.md", "# Nota")

            repository.delete_note("nota.md")

            with self.assertRaises(RepositoryError):
                repository.read_note("nota.md")


if __name__ == "__main__":
    unittest.main()
