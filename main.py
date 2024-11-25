from lsp_server.server import SigmaLanguageServer
from features.initialize import initialize
from features.diagnostics import publish_diagnostics
from lsprotocol.types import DidChangeTextDocumentParams
# Create the server instance
server = SigmaLanguageServer()

# Register the initialize feature


@server.feature("initialize")
def on_initialize(params):
    return initialize(server, params)

# Register the diagnostics feature
#@server.feature("textDocument/didChange")
#def on_did_change(params: DidChangeTextDocumentParams):
#    uri = params.textDocument.uri
#    content = params.contentChanges[0].text
#    publish_diagnostics(server, uri, content)

if __name__ == "__main__":
    server.start_io()
