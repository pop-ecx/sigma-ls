import unittest
import io
from ruamel.yaml.comments import CommentedMap, CommentedSeq
from features.structured_yaml_formatter import StructuredYAMLFormatter

class TestStructuredYAMLFormatter(unittest.TestCase):
    """
    test case for the StructuredYAMLFormatter class
    """
    def setUp(self):
        self.formatter = StructuredYAMLFormatter()

    def test_basic_formatting(self):
        """Test formatting of a well-formed Sigma rule"""
        input_yaml = """
        title: Test Rule
        logsource:
          category: test
        detection:
          selection:
            field: value
          condition: selection
        """
        expected = """title: Test Rule
logsource:
  category: test
detection:
  selection:
    field: value
  condition: selection
"""
        result = self.formatter.format_yaml(input_yaml)
        self.assertEqual(result.strip(), expected.strip())

    def test_string_logsource_conversion(self):
        """Test conversion of string logsource to proper structure"""
        input_yaml = """
        title: Test
        logsource: category:security,product:windows
        detection: {}
        """
        result = self.formatter.format_yaml(input_yaml)
        self.assertIn("category: security", result)
        self.assertIn("product: windows", result)
        self.assertIn("logsource:\n", result)

    def test_tags_formatting(self):
        """Test various tag formatting cases"""
        test_cases = [
            ('tags: "T1110,T1555"', ["T1110", "T1555"]),
            ('tags: [T1110, T1555]', ["T1110", "T1555"]),
            ('tags: ["T1110", "T1555"]', ["T1110", "T1555"]),
            ('tags: T1110', ["T1110"]),
        ]
        
        for input_yaml, expected_tags in test_cases:
            with self.subTest(input=input_yaml):
                full_yaml = f"""
                title: Test
                logsource: {{}}
                detection: {{}}
                {input_yaml}
                """
                result = self.formatter.format_yaml(full_yaml)
                for tag in expected_tags:
                    self.assertIn(f"- {tag}", result)

    def test_missing_required_fields(self):
        """Test that missing required fields are added"""
        input_yaml = "title: Test"
        result = self.formatter.format_yaml(input_yaml)
        self.assertIn("logsource: {}", result)
        self.assertIn("detection: {}", result)

    def test_detection_string_conversion(self):
        """Test string detection conversion"""
        input_yaml = """
        title: Test
        logsource: {}
        detection: selection:EventID=1
        """
        result = self.formatter.format_yaml(input_yaml)
        self.assertIn("selection: EventID=1", result)
        self.assertIn("detection:\n", result)

    def test_empty_document(self):
        """Test handling of empty YAML"""
        result = self.formatter.format_yaml("")
        self.assertEqual(result, "\n")

    def test_invalid_yaml(self):
        """Test error handling for invalid YAML"""
        with self.assertRaises(ValueError):
            self.formatter.format_yaml("invalid: yaml: : :")

    def test_complex_structure(self):
        """Test complex Sigma rule formatting"""
        input_yaml = """
        title: Complex Rule
        id: abc123
        logsource: 
          category: security
          product: windows
        detection:
          selection1:
            Field1: Value1
          selection2:
            Field2: Value2
          condition: selection1 and selection2
        level: high
        tags: [T1110, T1555]
        """
        result = self.formatter.format_yaml(input_yaml)
        self.assertIn("condition: selection1 and selection2", result)
        self.assertIn("- T1110", result)
        self.assertIn("- T1555", result)
        lines = result.splitlines()
        self.assertTrue(any(line.startswith("    Field1: Value1") for line in lines))

if __name__ == '__main__':
    unittest.main()
