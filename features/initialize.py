"""
Initialize deeznuts
"""
from lsprotocol.types import (
    InitializeParams,
    InitializeResult,
    TextDocumentSyncKind,
    CodeActionOptions,
    CodeActionKind
)

#@server.feature("initialize")
def initialize(params: InitializeParams) -> InitializeResult:
    """Initparams that returns initresults"""
    capabilities = {
        "textDocumentSync": TextDocumentSyncKind.Full,
        "diagnosticProvider": True,
        "codeActionProvider": CodeActionOptions(
            code_action_kinds=[
                CodeActionKind.QuickFix,
                CodeActionKind.Refactor,
                CodeActionKind.Source,
            ]
        ),
    }
    return InitializeResult(capabilities=capabilities)
