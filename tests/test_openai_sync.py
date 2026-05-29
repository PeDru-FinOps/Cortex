import tempfile
import unittest
from unittest.mock import patch

from cortex_notes.openai_sync import collect_local_note_files, sync_notes_to_openai
from cortex_notes.repository import NoteRepository


class FakeFile:
    def __init__(self, file_id):
        self.id = file_id


class FakeFiles:
    def __init__(self):
        self.created = []
        self.deleted = []

    def create(self, file, purpose):
        file_id = f"file_{len(self.created) + 1}"
        self.created.append({"id": file_id, "name": file.name, "purpose": purpose})
        return FakeFile(file_id)

    def delete(self, file_id):
        self.deleted.append(file_id)


class FakeVectorStoreFile:
    def __init__(self, file_id):
        self.id = file_id


class FakeVectorStoreFiles:
    def __init__(self):
        self.created = []
        self.deleted = []

    def create(self, vector_store_id, file_id, attributes):
        self.created.append(
            {"vector_store_id": vector_store_id, "file_id": file_id, "attributes": attributes}
        )
        return FakeVectorStoreFile(file_id)

    def delete(self, vector_store_id, file_id):
        self.deleted.append({"vector_store_id": vector_store_id, "file_id": file_id})


class FakeVectorStores:
    def __init__(self):
        self.files = FakeVectorStoreFiles()


class FakeOpenAI:
    instance = None

    def __init__(self, api_key):
        self.api_key = api_key
        self.files = FakeFiles()
        self.vector_stores = FakeVectorStores()
        FakeOpenAI.instance = self


class OpenAISyncTest(unittest.TestCase):
    def test_collect_local_note_files_hashes_markdown(self):
        with tempfile.TemporaryDirectory() as folder:
            repository = NoteRepository(folder)
            repository.write_note("a.md", "# A")

            files = collect_local_note_files(repository)

            self.assertEqual(files[0].path, "a.md")
            self.assertEqual(len(files[0].sha256), 64)

    def test_sync_uploads_and_then_skips_unchanged_files(self):
        with tempfile.TemporaryDirectory() as folder:
            repository = NoteRepository(folder)
            repository.write_note("a.md", "# A")

            with patch.dict(
                "os.environ",
                {
                    "OPENAI_API_KEY": "key",
                    "OPENAI_VECTOR_STORE_ID": "vs_test",
                    "CORTEX_SYNC_ROOT": f"{folder}/.sync",
                },
            ):
                first = sync_notes_to_openai(repository, client=FakeOpenAI("key"))
                second = sync_notes_to_openai(repository, client=FakeOpenAI("key"))

            self.assertEqual(first["uploaded"], ["a.md"])
            self.assertEqual(second["skipped"], ["a.md"])

    def test_sync_reuploads_changed_files(self):
        with tempfile.TemporaryDirectory() as folder:
            repository = NoteRepository(folder)
            repository.write_note("a.md", "# A")

            with patch.dict(
                "os.environ",
                {
                    "OPENAI_API_KEY": "key",
                    "OPENAI_VECTOR_STORE_ID": "vs_test",
                    "CORTEX_SYNC_ROOT": f"{folder}/.sync",
                },
            ):
                sync_notes_to_openai(repository, client=FakeOpenAI("key"))
                repository.write_note("a.md", "# A alterado")
                result = sync_notes_to_openai(repository, client=FakeOpenAI("key"))

            self.assertEqual(result["updated"], ["a.md"])


if __name__ == "__main__":
    unittest.main()
