from ruamel.yaml import YAML
from ruamel.yaml.compat import StringIO
from jsonschema import validate, ValidationError
from lsprotocol.types import Diagnostic, DiagnosticSeverity, Range, Position

# JSON schema for Sigma rules validation
SIGMA_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "logsource": {
            "type": "object",
            "properties": {
                "category": {"type": "string"},
                "product": {"type": "string"},
            },
            "required": ["category"],
        },
        "detection": {"type": "object"},
    },
    "required": ["title", "logsource", "detection"],
}

yaml = YAML()

def extract_key_line_mapping(content):
    """Map keys to their line numbers in the YAML document."""
    key_lines = {}
    stream = StringIO(content)
    yaml_obj = yaml.compose(stream)  # Parses without loading into Python structures

    def traverse(node):
        """Recursively traverse the YAML node."""
        if hasattr(node, "value"):  # Only process nodes with values
            if isinstance(node.value, list):  # Handle mappings
                for pair in node.value:
                    if len(pair) == 2:  # Ensure it's a key-value pair
                        key, value = pair
                        if hasattr(key, "start_mark"):
                            key_lines[key.value] = key.start_mark.line
                        traverse(value)
            elif isinstance(node.value, str):  # Handle scalar strings
                pass  # Scalars don’t need traversal

    if yaml_obj:
        traverse(yaml_obj)

    return key_lines

def validate_sigma(content: str):
    """Validate a Sigma rule's YAML content line by line."""
    diagnostics = []

    try:
        # Parse YAML content
        rule = yaml.load(content)
        key_lines = extract_key_line_mapping(content)

        # Check against JSON schema
        try:
            validate(instance=rule, schema=SIGMA_SCHEMA)
        except ValidationError as e:
            diagnostics.append(
                Diagnostic(
                    range=Range(
                        start=Position(line=0, character=0),
                        end=Position(line=0, character=1),
                    ),
                    message=f"Schema validation error: {e.message}",
                    severity=DiagnosticSeverity.Error,
                )
            )

        # Validate recommended fields
        recommended_fields = ["id", "status", "description", "author"]
        for field in recommended_fields:
            line = key_lines.get(field, 0)  # Default to line 0 if line is unknown
            if field not in rule:
                diagnostics.append(
                    Diagnostic(
                        range=Range(
                            start=Position(line=line, character=0),
                            end=Position(line=line, character=1),
                        ),
                        message=f"Recommended field '{field}' is missing.",
                        severity=DiagnosticSeverity.Hint,
                    )
                )
            elif not isinstance(rule[field], str) or not rule[field].strip():
                diagnostics.append(
                    Diagnostic(
                        range=Range(
                            start=Position(line=line, character=0),
                            end=Position(line=line, character=len(field)),
                        ),
                        message=f"Field '{field}' must be a non-empty string.",
                        severity=DiagnosticSeverity.Warning,
                    )
                )

    except Exception as e:
        # Handle YAML parsing errors
        diagnostics.append(
            Diagnostic(
                range=Range(
                    start=Position(line=0, character=0),
                    end=Position(line=0, character=1),
                ),
                message=f"YAML parsing error: {str(e)}",
                severity=DiagnosticSeverity.Error,
            )
        )

    return diagnostics


def publish_diagnostics(server, uri, content):
    """Send diagnostics to the client."""
    diagnostics = validate_sigma(content)
    server.publish_diagnostics(uri, diagnostics)
