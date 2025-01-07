"""
code action features for language server
"""
import uuid
from lsprotocol.types import (
    CodeAction,
    CodeActionKind,
    TextEdit,
    Position,
    Range,
    WorkspaceEdit,
    TextDocumentEdit,
    VersionedTextDocumentIdentifier
)

def suggest_code_action(uri, diagnostics):
    """Suggest code actions based on diagnostics."""
    code_actions = []

    for diag in diagnostics:
        if "must be a valid UUID" in diag.message:
            # Suggest replacing invalid UUID
            new_uuid = str(uuid.uuid4())
            start_position = Position(line=diag.range.start.line, character=0)
            end_position = Position(line=diag.range.start.line + 1, character=0)
            text_edit = TextEdit(
                range=Range(start_position, end_position),
                new_text=f"id: {new_uuid}\n"
            )
            workspace_edit = WorkspaceEdit(
                document_changes=[
                    TextDocumentEdit(
                        text_document=VersionedTextDocumentIdentifier(uri=uri, version=0),
                        edits=[text_edit]
                    )
                ]
            )
            code_action = CodeAction(
                title="Replace with a valid UUID",
                kind=CodeActionKind.QuickFix,
                edit=workspace_edit
            )
            code_actions.append(code_action)
        elif "Recommended field" in diag.message:
            # Suggest adding the missing field
            missing_field = diag.message.split("'")[1]
            line = diag.range.start.line
            text_edit = TextEdit(
                range=Range(
                    start=Position(line=line, character=0),
                    end=Position(line=line, character=0)
                ),
                new_text=f"{missing_field}: \n"
            )
            workspace_edit = WorkspaceEdit(
                document_changes=[
                    TextDocumentEdit(
                        text_document=VersionedTextDocumentIdentifier(uri=uri, version=0),
                        edits=[text_edit]
                    )
                ]
            )
            code_action = CodeAction(
                title=f"Add missing field '{missing_field}'",
                kind=CodeActionKind.QuickFix,
                edit=workspace_edit
            )
            code_actions.append(code_action)

        elif "The title is too long" in diag.message:
            # Suggest truncating the title
            start_position = Position(line=diag.range.start.line, character=0)
            end_position = Position(line=diag.range.start.line + 1, character=0)
            line = diag.range.start.line
            text_edit = TextEdit(
                range=Range(start_position, end_position),
                new_text="title: Shortened Title\n"
            )
            workspace_edit = WorkspaceEdit(
                document_changes=[
                    TextDocumentEdit(
                        text_document=VersionedTextDocumentIdentifier(uri=uri, version=0),
                        edits=[text_edit]
                    )
                ]
            )
            code_action = CodeAction(
                title="Truncate the title",
                kind=CodeActionKind.QuickFix,
                edit=workspace_edit
            )
            code_actions.append(code_action)
        elif "Ensure the 'date' field is enclosed" in diag.message:
            # Suggest wrapping the date in quotes
            line = diag.range.start.line
            text_edit_start = TextEdit(
                range=Range(
                    start=Position(line=line, character=0),
                    end=Position(line=line, character=0)
                ),
                new_text='"'
            )
            text_edit_end = TextEdit(
                range=Range(
                    start=Position(line=line, character=len("date")),
                    end=Position(line=line, character=len("date"))
                ),
                new_text='"'
            )
            workspace_edit = WorkspaceEdit(
                document_changes=[
                    TextDocumentEdit(
                        text_document=VersionedTextDocumentIdentifier(uri=uri, version=0),
                        edits=[text_edit_start, text_edit_end]
                    )
                ]
            )
            code_action = CodeAction(
                title="Wrap the date in quotes",
                kind=CodeActionKind.QuickFix,
                edit=workspace_edit
            )
            code_actions.append(code_action)
    return code_actions

def provide_code_actions(server, params):
    """Provide code actions to the client."""
    uri = params.text_document.uri
    diagnostics = params.context.diagnostics
    code_actions = suggest_code_action(uri, diagnostics)
    return code_actions
