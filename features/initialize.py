"""
Initialize deeznuts
"""
from lsprotocol.types import InitializeParams, InitializeResult, TextDocumentSyncKind

#@server.feature("initialize")
def initialize(server, params: InitializeParams) -> InitializeResult:
    """Initparams that returns initresults"""
    capabilities = {
        "textDocumentSync": TextDocumentSyncKind.Full,
        "diagnosticProvider": True
    }
    return InitializeResult(capabilities=capabilities)
