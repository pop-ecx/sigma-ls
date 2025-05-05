"""
Import structured yaml formatter to format rules
"""
from lsprotocol.types import TextEdit, Range, Position, MessageType
from .structured_yaml_formatter import StructuredYAMLFormatter

def format_document(server, params):
    """Handle document formatting request"""
    try:
        document_uri = params.text_document.uri
        document = server.workspace.get_document(document_uri)
        if not document:
            return None

        formatter = StructuredYAMLFormatter()
        formatted_text = formatter.format_yaml(document.source)
        lines = document.source.splitlines()
        range_ = Range(
            start=Position(line=0, character=0),
            end=Position(
                line=len(lines)-1 if lines else 0,
                character=len(lines[-1]) if lines else 0
            )
        )
        return [TextEdit(range=range_, new_text=formatted_text)]
    except ValueError as err:
        server.show_message_log(f"Formatting error: {err}")
        server.show_message(str(err), msg_type=MessageType.Error)
        return []
    except Exception as err:
        server.show_message_log(f"Unexpected error: {err}")
        return []
