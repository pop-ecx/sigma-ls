"""
Diagnostics feature 
"""
import ruamel.yaml
from ruamel.yaml import YAML
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
    yaml_obj = yaml.compose(content)  # Parse yaml into a node structure

    def traverse(node):
        """Recursively traverse the YAML node."""
        if isinstance(node, ruamel.yaml.nodes.MappingNode):  # Process mappings
            for key_node, value_node in node.value:
                if isinstance(key_node, ruamel.yaml.nodes.ScalarNode):
                    key_lines[key_node.value] = key_node.start_mark.line
                traverse(value_node)
        elif isinstance(node, ruamel.yaml.nodes.SequenceNode):
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
        rule = yaml.load(content)
        key_lines = extract_key_line_mapping(content)

        # Check against JSON schema
        try:
            validate(instance=rule, schema=SIGMA_SCHEMA)
        except ValidationError as validation_error:
            diagnostics.append(
                Diagnostic(
                    range=Range(
                        start=Position(line=0, character=0),
                        end=Position(line=0, character=1),
                    ),
                    message=f"Schema validation error: {validation_error.message}",
                    severity=DiagnosticSeverity.Error,
                )
            )

        # Validate recommended fields
        recommended_fields = ["id", "status", "description", "author"]
        for field in recommended_fields:
            line = key_lines.get(field, 0)
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

        # Hawk is bitchy if date is not wrapped
        if "date" in rule:
            date_value = rule["date"]
            date_line = key_lines.get("date", 0)
            if not (isinstance(date_value, str) and date_value.startswith('"') and date_value.endswith('"')):
                diagnostics.append(
                        Diagnostic(
                            range=Range(
                                start=Position(line=date_line, character=0),
                                end=Position(line=date_line, character=len("date")),
                            ),
                            message="Ensure the 'date' field is enclosed in quotation marks if planning to use the Hawk backend",
                            severity=DiagnosticSeverity.Hint,
                        )
                    )

        # Custom validation for logsource with product or service as okta
        if "logsource" in rule:
            logsource = rule["logsource"]
            if (
                isinstance(logsource, dict)
                and logsource.get("product") == "okta"
                or logsource.get("service") == "okta"
            ):
                logsource_line = key_lines.get("logsource", 0)
                diagnostics.append(
                    Diagnostic(
                        range=Range(
                            start=Position(line=logsource_line, character=0),
                            end=Position(line=logsource_line, character=len("logsource")),
                        ),
                        message="Lacework backend does not support logsource 'okta'.",
                        severity=DiagnosticSeverity.Warning,
                    )
                )

    except Exception as parsing_error:
        # Handle YAML parsing errors
        diagnostics.append(
            Diagnostic(
                range=Range(
                    start=Position(line=0, character=0),
                    end=Position(line=0, character=1),
                ),
                message=f"YAML parsing error: {str(parsing_error)}",
                severity=DiagnosticSeverity.Error,
            )
        )

    return diagnostics


def publish_diagnostics(server, uri, content):
    """Send diagnostics to the client."""
    diagnostics = validate_sigma(content)
    server.publish_diagnostics(uri, diagnostics)
