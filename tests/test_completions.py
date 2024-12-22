"""
Test for completions
"""
import unittest
from lsprotocol.types import CompletionParams
from features.completions import register_completion_feature

class TestCompletions(unittest.TestCase):
    """
    create a class for completions test
    """
    def setUp(self):
        # Mock server object
        class MockServer:
            """
            Create a mock server
            """
            def feature(self, feature_name):
                """
                feature
                """
                def decorator(func):
                    self.feature_function = func
                    return func
                return decorator

        self.server = MockServer()
        register_completion_feature(self.server)

    def test_completions(self):
        """
        test completions function
        """
        # Mock CompletionParams
        params = CompletionParams(
            text_document={"uri": "file://mock_file.sigma"},
            position={"line": 0, "character": 0}
        )

        # Invoke the registered completion feature
        completions = self.server.feature_function(params)
        self.assertIsInstance(completions, list)
        self.assertGreater(len(completions), 0)

        # Test specific completion items
        titles = [item.label for item in completions]
        self.assertIn("title", titles)
        self.assertIn("logsource", titles)

if __name__ == "__main__":
    unittest.main()
