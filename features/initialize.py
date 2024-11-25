from lsprotocol.types import InitializeParams, InitializeResult

#@server.feature("initialize")
def initialize(params: InitializeParams) -> InitializeResult:
    capabilities = {
        "textDocumentSync": TextDocumentSyncKind.Full,
        "diagnosticProvider": True
    }
    return InitializeResult(capabilities=capabilities)
