"""
Main module for the Sigma Language Server.
Handles initialization, document change, and diagnostic features.
"""
from lsprotocol.types import (DidChangeTextDocumentParams,
    TEXT_DOCUMENT_DID_OPEN,
    TEXT_DOCUMENT_DID_CHANGE,
    DidOpenTextDocumentParams)
from lsp_server.server import SigmaLanguageServer
from features.initialize import initialize
from features.diagnostics import publish_diagnostics
from features.completions import register_completion_feature
from features.mitre_fetcher import search_mitre 

# Create the server instance
server = SigmaLanguageServer()

# Register the initialize feature
@server.feature("initialize")
def on_initialize(params):
    """Handle initialize request"""
    return initialize(server, params)

# Handle file opening
@server.feature(TEXT_DOCUMENT_DID_OPEN)
def did_open(params: DidOpenTextDocumentParams):
    """Detect if client opened document"""
    uri = params.text_document.uri
    content = server.workspace.get_text_document(uri).source  # Access server instance directly
    publish_diagnostics(server, uri, content)

@server.feature(TEXT_DOCUMENT_DID_CHANGE)
def did_change(params: DidChangeTextDocumentParams):
    """detect if opened text changed"""
    uri = params.text_document.uri
    content = server.workspace.get_text_document(uri).source
    publish_diagnostics(server, uri, content)

@server.feature("sigma/searchMitre")
def handle_mitre_search(params):
    """
    search mitre tags locally
    """
    return search_mitre(params)

register_completion_feature(server)
if __name__ == "__main__":
    server.start_io()
