"""
Main module for the Sigma Language Server.
Handles initialization, document change, and diagnostic features.
"""
from lsprotocol.types import (DidChangeTextDocumentParams,
    TEXT_DOCUMENT_DID_OPEN,
    TEXT_DOCUMENT_DID_CHANGE,
    TEXT_DOCUMENT_FORMATTING,
    Hover,
    HoverParams,
    DidOpenTextDocumentParams,
    CodeActionParams,
    DocumentSymbol
)
from lsp_server.server import SigmaLanguageServer
from features.initialize import initialize
from features.diagnostics import publish_diagnostics
from features.completions import register_completion_feature
from features.mitre_fetcher import search_mitre
from features.hover import handle_hover
from features.codeActions import provide_code_actions
from features.document_symbols import parse_sigma_symbols
from features.document_symbols import provide_document_symbols
from features.formatter import format_document

# Create the server instance
server = SigmaLanguageServer()

# Register the initialize feature
@server.feature("initialize")
def on_initialize(params):
    """Handle initialize request"""
    return initialize(params)

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

@server.feature("textDocument/codeAction")
def code_action(params: CodeActionParams):
    """Provide code actions based on diagnostics"""
    return provide_code_actions(server, params)

@server.feature("sigma/searchMitre")
def handle_mitre_search(params):
    """
    search mitre tags locally
    """
    return search_mitre(params)

@server.feature("textDocument/hover")
def hover_feature(server: SigmaLanguageServer, params: HoverParams) -> Hover:
    """
    Handle hover request
    """
    return handle_hover(server, params)

@server.feature("textDocument/documentSymbol")
def document_symbol(params):
    """Provide document symbols for Sigma rules"""
    return provide_document_symbols(server, params)

@server.feature(TEXT_DOCUMENT_FORMATTING)
def formatting_feature(params):
    """Handle document formatting"""
    return format_document(server, params)

register_completion_feature(server)

if __name__ == "__main__":
    server.start_io()
