import tempfile
import unittest

from cortex_notes.graph import build_local_graph, extract_tags, extract_wiki_links, resolve_wiki_link
from cortex_notes.markdown_render import render_markdown
from cortex_notes.repository import NoteRepository


class GraphTest(unittest.TestCase):
    def test_extract_tags_normalizes_and_deduplicates(self):
        content = "# Titulo sem tag\nTexto com #Python #python #area/projeto e email#aqui."

        self.assertEqual(extract_tags(content), {"python", "area/projeto"})

    def test_extract_wiki_links_supports_aliases(self):
        content = "Veja [[Minha Nota]] e [[pasta/outra.md|Outra]]."

        self.assertEqual(extract_wiki_links(content), {"Minha Nota", "pasta/outra.md"})

    def test_resolve_wiki_link_matches_stem_or_path(self):
        lookup = {
            "area/minha nota.md": "area/Minha Nota.md",
            "area/minha nota": "area/Minha Nota.md",
            "minha nota": "area/Minha Nota.md",
        }

        self.assertEqual(resolve_wiki_link("Minha Nota", lookup), "area/Minha Nota.md")

    def test_markdown_renders_hash_without_space_as_tag_label(self):
        html = render_markdown("#cloud8\n\nTexto", {})

        self.assertIn('class="tag-label"', html)
        self.assertNotIn("<h1>", html)

    def test_markdown_renders_wiki_link_to_note(self):
        lookup = {"untagged": "Cloud8/Funcionalidades/Untagged.md"}

        html = render_markdown("Veja [[Untagged]].", lookup)

        self.assertIn('class="wiki-link"', html)
        self.assertIn("Cloud8/Funcionalidades/Untagged.md", html)

    def test_markdown_renders_obsidian_image_links(self):
        html = render_markdown(
            "![[Pasted image 1.png]]",
            {},
            image_resolver=lambda target: "assets/Pasted image 1.png",
        )

        self.assertIn('class="note-image"', html)
        self.assertIn("/assets?path=assets/Pasted%20image%201.png", html)

    def test_markdown_marks_missing_obsidian_image_links(self):
        html = render_markdown("![[Pasted image 1.png]]", {}, image_resolver=lambda target: None)

        self.assertIn('class="image-missing"', html)
        self.assertNotIn('class="wiki-link"', html)

    def test_build_local_graph_keeps_only_direct_connections(self):
        with tempfile.TemporaryDirectory() as folder:
            repository = NoteRepository(folder)
            repository.write_note("a.md", "#tag [[b]]")
            repository.write_note("b.md", "#outra")
            repository.write_note("c.md", "#fora")

            graph = build_local_graph(repository, "a.md")
            node_ids = {node["id"] for node in graph["nodes"]}

            self.assertIn("note:a.md", node_ids)
            self.assertIn("note:b.md", node_ids)
            self.assertIn("tag:tag", node_ids)
            self.assertNotIn("note:c.md", node_ids)


if __name__ == "__main__":
    unittest.main()
