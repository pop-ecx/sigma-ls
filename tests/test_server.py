"""
test case for the server
"""
import unittest
from lsp_server.server import SigmaLanguageServer

class TestServer(unittest.TestCase):
    """
    test server class
    """
    def test_server_initialization(self):
        """
        test server initialization
        """
        server = SigmaLanguageServer()
        self.assertIsNotNone(server)
        self.assertTrue(hasattr(server, "start_io"))
        self.assertTrue(callable(getattr(server, "start_io", None)))
if __name__ == "__main__":
    unittest.main()
