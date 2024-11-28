import ruamel.yaml
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
                "service": {"type": "string"},
            },
        },
        "detection": {"type": "object"},
    },
    "required": ["title", "logsource", "detection"],
}

yaml = YAML()

def extract_key_line_mapping(content):
    """Map keys to their line numbers in the YAML document."""
    key_lines = {}
    yaml = YAML()
    yaml_obj = yaml.compose(content)  # Parse yaml into a node structure

    def traverse(node):
        """Recursively traverse the YAML node."""
        if isinstance(node, ruamel.yaml.nodes.MappingNode):  # Process mappings
            for key_node, value_node in node.value:
                if isinstance(key_node, ruamel.yaml.nodes.ScalarNode):  # Key must be a scalar
                    key_lines[key_node.value] = key_node.start_mark.line
                traverse(value_node)  # Recursively process the value node
        elif isinstance(node, ruamel.yaml.nodes.SequenceNode):  # Process sequences (lists)
            for item in node.value:
                traverse(item)
        elif isinstance(node, ruamel.yaml.nodes.ScalarNode):  # Scalars (values) don't need traversal duh
            pass

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
            line = key_lines.get(field, 0)  # Default to line 0 if line is unknown gave me headaches
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
