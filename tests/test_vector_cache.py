import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from cortex_notes.vector_cache import (
    cache_summary,
    load_vector_cache,
    read_openai_vector_store_to_cache,
    save_vector_cache,
    search_vector_cache,
)


class VectorCacheTest(unittest.TestCase):
    def test_save_load_and_search_vector_cache(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            save_vector_cache(
                root,
                {
                    "vector_store_id": "vs_test",
                    "created_at": 123,
                    "document_count": 1,
                    "documents": [
                        {
                            "file_id": "file_1",
                            "filename": "FinOps Tags.md",
                            "text": "Tags ajudam na alocacao de custos cloud.",
                        }
                    ],
                },
            )

            cache = load_vector_cache(root)
            results = search_vector_cache(root, "custos tags")
            summary = cache_summary(cache)

            self.assertTrue(summary["available"])
            self.assertTrue(summary["usable"])
            self.assertEqual(summary["documents_with_text"], 1)
            self.assertEqual(results[0]["source"], "openai-vector-cache")
            self.assertEqual(results[0]["path"], "FinOps Tags.md")

    def test_cache_summary_marks_empty_cache_as_unusable(self):
        cache = {
            "vector_store_id": "vs_test",
            "created_at": 123,
            "document_count": 1,
            "documents": [
                {
                    "file_id": "file_1",
                    "filename": "FinOps Tags.md",
                    "text": "",
                    "error": "Not allowed to download files of purpose: assistants",
                }
            ],
        }

        summary = cache_summary(cache)

        self.assertTrue(summary["available"])
        self.assertFalse(summary["usable"])
        self.assertEqual(summary["documents_with_text"], 0)
        self.assertEqual(summary["documents_with_errors"], 1)

    def test_read_reuses_usable_cache_without_remote_calls(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            save_vector_cache(
                root,
                {
                    "vector_store_id": "vs_test",
                    "created_at": 123,
                    "document_count": 1,
                    "documents": [
                        {
                            "file_id": "file_1",
                            "filename": "FinOps Tags.md",
                            "text": "conteudo em cache",
                        }
                    ],
                },
            )

            with patch.dict("os.environ", {"OPENAI_API_KEY": "test", "OPENAI_VECTOR_STORE_ID": "vs_test"}):
                summary = read_openai_vector_store_to_cache(root, client=ExplodingClient())

            self.assertTrue(summary["reused"])
            self.assertTrue(summary["usable"])

    def test_read_uses_vector_store_file_content_endpoint(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            client = FakeOpenAIClient()

            with patch.dict("os.environ", {"OPENAI_API_KEY": "test", "OPENAI_VECTOR_STORE_ID": "vs_test"}):
                summary = read_openai_vector_store_to_cache(root, client=client, force=True)
            results = search_vector_cache(root, "custos")

            self.assertTrue(summary["usable"])
            self.assertEqual(client.vector_stores.files.content_calls, 1)
            self.assertEqual(results[0]["source"], "openai-vector-cache")


class ExplodingClient:
    @property
    def vector_stores(self):
        raise AssertionError("Remote client should not be used when cache is reusable.")


class FakeFile:
    id = "file_1"


class FakeRetrievedFile:
    filename = "FinOps Tags.md"


class FakeContentPart:
    def __init__(self, text):
        self.text = text


class FakeContentPage:
    def __iter__(self):
        return iter([FakeContentPart("Tags ajudam na alocacao de custos cloud.")])


class FakeVectorStoreFiles:
    def __init__(self):
        self.content_calls = 0

    def list(self, vector_store_id, limit):
        return [FakeFile()]

    def content(self, file_id, vector_store_id):
        self.content_calls += 1
        return FakeContentPage()


class FakeVectorStores:
    def __init__(self):
        self.files = FakeVectorStoreFiles()


class FakeFiles:
    def retrieve(self, file_id):
        return FakeRetrievedFile()


class FakeOpenAIClient:
    def __init__(self):
        self.vector_stores = FakeVectorStores()
        self.files = FakeFiles()


if __name__ == "__main__":
    unittest.main()
