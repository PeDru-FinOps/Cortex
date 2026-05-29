import tempfile
import unittest
from pathlib import Path

from cortex_notes.connection_rejections import is_rejected, load_rejections, reject_connection


class ConnectionRejectionTest(unittest.TestCase):
    def test_reject_connection_is_bidirectional(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            data = reject_connection(root, "a.md", "b.md", "nao faz sentido")

            rejections = load_rejections(root)

            self.assertEqual(data["source"], "a.md")
            self.assertTrue(is_rejected(rejections, "a.md", "b.md"))
            self.assertTrue(is_rejected(rejections, "b.md", "a.md"))


if __name__ == "__main__":
    unittest.main()
