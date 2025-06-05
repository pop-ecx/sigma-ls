"""
Format sigma rules to a structured YAML format.
"""
import io
from typing import Any, Dict
import ruamel.yaml
from ruamel.yaml.comments import CommentedMap, CommentedSeq

class StructuredYAMLFormatter:
    def __init__(self):
        """
        Initialize
        """
        self.yaml = ruamel.yaml.YAML()
        self.yaml.indent(mapping=2, sequence=4, offset=2)
        self.yaml.preserve_quotes = True
        self.yaml.width = 4096
        self.schema = {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "logsource": {
                    "type": "object",
                    "properties": {
                        "category": {"type": "string"},
                        "product": {"type": "string"},
                        "service": {"type": "string"},
                    },
                },
                "detection": {"type": "object"},
            },
            "required": ["title", "logsource", "detection"]
        }
    def ensure_structure(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Ensure the YAML matches the defined structure while preserving content"""
        if not isinstance(data, dict):
            return data
        for field in self.schema["required"]:
            if field not in data:
                if field == "logsource":
                    data[field] = CommentedMap()
                elif field == "detection":
                    data[field] = CommentedMap()
                else:
                    data[field] = ""
        if "logsource" in data:
            if isinstance(data["logsource"], str):
                new_logsource = CommentedMap()
                if ":" in data["logsource"]:
                    for item in data["logsource"].split(","):
                        if ":" in item:
                            key, value = item.split(":", 1)
                            new_logsource[key.strip()] = value.strip()
                else:
                    new_logsource["category"] = data["logsource"].strip()
                data["logsource"] = new_logsource
        if "detection" in data:
            if isinstance(data["detection"], str):
                new_detection = CommentedMap()
                if ":" in data["detection"]:
                    key, value = data["detection"].split(":", 1)
                    new_detection[key.strip()] = value.strip()
                else:
                    new_detection[data["detection"].strip()] = None
                data["detection"] = new_detection
        if "tags" in data:
            if isinstance(data["tags"], str):
                data["tags"] = [tag.strip() for tag in data["tags"].split(",")]
            elif isinstance(data["tags"], (list, CommentedSeq)):
                cleaned_tags = []
                for tag in data["tags"]:
                    if isinstance(tag, str):
                        cleaned_tags.append(tag.strip())
                    else:
                        cleaned_tags.append(str(tag))
                data["tags"] = CommentedSeq(cleaned_tags)
            else:
                data["tags"] = CommentedSeq()
        return data
    def format_yaml(self, text: str) -> str:
        """Format YAML text according to the defined structure"""
        try:
            data = self.yaml.load(text)
            if data is None:
                return text
            data = self.ensure_structure(data)
            output = io.StringIO()
            self.yaml.dump(data, output)
            formatted = output.getvalue()
            formatted = "\n".join(line.rstrip() for line in formatted.splitlines())
            if not formatted.endswith("\n"):
                formatted += "\n"
            return formatted
        except Exception as e:
            raise ValueError(f"YAML formatting error: {str(e)}")
