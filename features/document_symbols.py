"""
Document Symbols Feature
"""
from lsprotocol.types import DocumentSymbol, SymbolKind, Position, Range
from ruamel.yaml import YAML

yaml = YAML()  # Create ruamel.yaml instance

def parse_sigma_symbols(content):
    """
    Parses a Sigma rule and extracts document symbols.
    """
    print("Parsing Sigma Symbols...")  # Debugging line
    symbols = []

    try:
        parsed_yaml = yaml.load(content)  # ruamel.yaml parsing
        if not isinstance(parsed_yaml, dict):
            return symbols

        lines = content.splitlines()

        for key, value in parsed_yaml.items():
            # Find the line where this key appears
            line_num = next((i for i, line in enumerate(lines) if line.strip().startswith(f"{key}:")), 0)

            start_pos = Position(line=line_num, character=0)
            end_pos = Position(line=line_num, character=len(key))

            if isinstance(value, dict):
                kind = SymbolKind.Module  # Represent nested dictionaries as modules
            elif isinstance(value, list):
                kind = SymbolKind.Array  # Lists are arrays
            else:
                kind = SymbolKind.Field  # Everything else is a field

            symbol = DocumentSymbol(
                name=key,
                kind=kind,
                range=Range(start=start_pos, end=end_pos),
                selection_range=Range(start=start_pos, end=end_pos),
            )
            symbols.append(symbol)

    except Exception as parse_error:
        print(f"YAML Parsing Error: {parse_error}")  # Debugging line

    print(f"Symbols found: {symbols}")  # Debugging line
    return symbols

def provide_document_symbols(server, params):
    """Provide document symbols for outline view."""
    uri = params.text_document.uri
    content = server.workspace.get_text_document(uri).source
    print(f"Processing Document: {uri}")  # Debugging line
    return parse_sigma_symbols(content)
