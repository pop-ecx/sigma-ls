import yaml
import jsonschema
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
                "product": {"type": "string"}
            },
            "required": ["category"]
        },
        "detection": {"type": "object"},
        "condition": {"type": "string"}
    },
    "required": ["title", "logsource", "detection", "condition"]
}

def validate_sigma(content: str):
    """Validate a Sigma rule's YAML content."""
    diagnostics = []

    try:
        rule = yaml.safe_load(content)
        jsonschema.validate(instance=rule, schema=SIGMA_SCHEMA)

    except yaml.YAMLError as e:
        diagnostics.append(Diagnostic(
            range={"start": {"line": 0, "character": 0}, "end": {"line": 0, "character": 1}},
            message=f"YAML parsing error: {str(e)}",
            severity=DiagnosticSeverity.Error
        ))

    except jsonschema.ValidationError as e:
        diagnostics.append(Diagnostic(
            range={"start": {"line": 0, "character": 0}, "end": {"line": 0, "character": 1}},
            message=f"Schema validation error: {str(e.message)}",
            severity=DiagnosticSeverity.Error
        ))

    return diagnostics

# Wrote this while GNX was on a loop. Luther is a vibe y'all :D
def publish_diagnostics(server, uri, content):
    diagnostics = []

    try:
        # Parse the YAML content
        rule = yaml.safe_load(content)

        # Check if required fields are missing
        required_fields = ["detection", "logsource", "title"]
        for field in required_fields:
            if field not in rule:
                diagnostics.append(
                    Diagnostic(
                        range=Range(
                            start=Position(line=0, character=0),
                            end=Position(line=0, character=1),
                        ),
                        message=f"Missing required field: '{field}'.",
                        severity=DiagnosticSeverity.Error,
                    )
                )

    except yaml.YAMLError as e:
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

    # Publish diagnostics to the client
    server.publish_diagnostics(uri, diagnostics)

