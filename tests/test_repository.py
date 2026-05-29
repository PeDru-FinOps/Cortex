import tempfile
import unittest
from io import BytesIO

from cortex_notes.repository import NoteRepository, RepositoryError
from app import approved_article_content, next_article_path


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

    def test_import_file_stream_accepts_images(self):
        with tempfile.TemporaryDirectory() as folder:
            repository = NoteRepository(folder)

            imported = repository.import_file_stream("Anexos/imagem.png", BytesIO(b"png"))

            self.assertEqual(imported, "Anexos/imagem.png")
            self.assertEqual(repository.resolve_asset_path(imported).read_bytes(), b"png")

    def test_find_attachment_by_filename(self):
        with tempfile.TemporaryDirectory() as folder:
            repository = NoteRepository(folder)
            repository.import_file_stream("Anexos/imagem.png", BytesIO(b"png"))

            self.assertEqual(repository.find_attachment("imagem.png"), "Anexos/imagem.png")

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

    def test_copy_note_creates_unique_copy(self):
        with tempfile.TemporaryDirectory() as folder:
            repository = NoteRepository(folder)
            repository.write_note("area/nota.md", "# Nota")

            first = repository.copy_note("area/nota.md")
            second = repository.copy_note("area/nota.md")

            self.assertEqual(first, "area/nota - copia.md")
            self.assertEqual(second, "area/nota - copia 2.md")
            self.assertEqual(repository.read_note(first)["content"], "# Nota")

    def test_delete_folder_removes_folder(self):
        with tempfile.TemporaryDirectory() as folder:
            repository = NoteRepository(folder)
            repository.write_note("area/nota.md", "# Nota")

            parent = repository.delete_folder("area")

            self.assertEqual(parent, "")
            with self.assertRaises(RepositoryError):
                repository.read_note("area/nota.md")

    def test_append_note_link_adds_approved_connections_section(self):
        with tempfile.TemporaryDirectory() as folder:
            repository = NoteRepository(folder)
            repository.write_note("a.md", "# A")
            repository.write_note("b.md", "# B")

            result = repository.append_note_link("a.md", "b.md")
            content = repository.read_note("a.md")["content"]

            self.assertTrue(result["changed"])
            self.assertIn("## Conexoes aprovadas", content)
            self.assertIn("[[b]]", content)

    def test_append_note_link_does_not_duplicate_existing_link(self):
        with tempfile.TemporaryDirectory() as folder:
            repository = NoteRepository(folder)
            repository.write_note("a.md", "# A\n\n[[b]]")
            repository.write_note("b.md", "# B")

            result = repository.append_note_link("a.md", "b.md")

            self.assertFalse(result["changed"])

    def test_approve_connection_adds_links_to_both_notes(self):
        with tempfile.TemporaryDirectory() as folder:
            repository = NoteRepository(folder)
            repository.write_note("a.md", "# A")
            repository.write_note("b.md", "# B")

            result = repository.approve_connection("a.md", "b.md")

            self.assertTrue(result["changed"])
            self.assertIn("[[b]]", repository.read_note("a.md")["content"])
            self.assertIn("[[a]]", repository.read_note("b.md")["content"])

    def test_next_article_path_uses_artigos_and_avoids_collision(self):
        with tempfile.TemporaryDirectory() as folder:
            repository = NoteRepository(folder)
            repository.create_folder("Artigos")
            repository.write_note("Artigos/linkedin-finops.md", "# Existente")

            path = next_article_path(repository, "FinOps", "linkedin")

            self.assertEqual(path, "Artigos/linkedin-finops-2.md")

    def test_approved_article_content_preserves_edited_text(self):
        self.assertEqual(approved_article_content("  Texto editado\n\n"), "Texto editado\n")

    def test_approved_article_content_appends_tags(self):
        self.assertEqual(
            approved_article_content("# Artigo", ["FinOps", "#Azure"]),
            "# Artigo\n\n#finops #azure\n",
        )

    def test_append_tags_adds_only_new_tags(self):
        with tempfile.TemporaryDirectory() as folder:
            repository = NoteRepository(folder)
            repository.write_note("a.md", "# A\n\n#finops")

            result = repository.append_tags("a.md", ["finops", "azure"])
            content = repository.read_note("a.md")["content"]

            self.assertTrue(result["changed"])
            self.assertEqual(result["tags"], ["azure"])
            self.assertIn("#azure", content)


if __name__ == "__main__":
    unittest.main()
