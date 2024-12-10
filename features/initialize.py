"""
Initialize deeznuts
"""
from lsprotocol.types import InitializeParams, InitializeResult

#@server.feature("initialize")
def initialize(params: InitializeParams) -> InitializeResult:
    """Initparams that returns initresults"""
    capabilities = {
        "textDocumentSync": TextDocumentSyncKind.Full,
        "diagnosticProvider": True
    }
    return InitializeResult(capabilities=capabilities)
