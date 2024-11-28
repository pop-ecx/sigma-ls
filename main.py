from lsp_server.server import SigmaLanguageServer
from features.initialize import initialize
from features.diagnostics import publish_diagnostics
from lsprotocol.types import DidChangeTextDocumentParams, TEXT_DOCUMENT_DID_OPEN, TEXT_DOCUMENT_DID_SAVE, TEXT_DOCUMENT_DID_CHANGE, DidOpenTextDocumentParams, DidSaveTextDocumentParams
from features.completions import register_completion_feature

# Create the server instance
server = SigmaLanguageServer()

# Register the initialize feature
@server.feature("initialize")
def on_initialize(params):
    return initialize(server, params)

# Handle file opening
@server.feature(TEXT_DOCUMENT_DID_OPEN)
def did_open(params: DidOpenTextDocumentParams):  
    uri = params.text_document.uri
    content = server.workspace.get_document(uri).source  # Access server instance directly
    publish_diagnostics(server, uri, content)

@server.feature(TEXT_DOCUMENT_DID_CHANGE)
def did_change(params: DidChangeTextDocumentParams):
    uri = params.text_document.uri
    content = server.workspace.get_document(uri).source
    publish_diagnostics(server, uri, content)

register_completion_feature(server)
if __name__ == "__main__":
    server.start_io()
