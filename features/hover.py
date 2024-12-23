"""
get hover information for a given word
"""
from lsprotocol.types import Hover, TextDocumentPositionParams
import json
import os

def load_mitre_attack_data():
    file_path = os.path.join(os.path.dirname(__file__), "mitre_attack.json")
    with open(file_path, "r") as f:
        return json.load(f)

MITRE_ATTACK_DATA = load_mitre_attack_data()

def get_hover_content(word: str) -> str:
    """Get hover content for a given word."""
    hover_data = {
        "EventID": "Windows Event ID. E.g., 4625 represents failed logon attempts.",
        "selection": "The Sigma detection field used for matching log patterns.",
    }

    # Check MITRE ATT&CK data for additional context
    for entry in MITRE_ATTACK_DATA:
        if entry["tag"] == word:
            return f"{entry['description']}\n\n**Reference:** [View more]({entry['url']})"

    return hover_data.get(word, f"No additional information available for '{word}'.")


def handle_hover(server, params: TextDocumentPositionParams) -> Hover:
    """Handles hover requests."""
    document = server.workspace.get_document(params.text_document.uri)
    position = params.position

    line_content = document.lines[position.line]
    word_start = max(line_content.rfind(" ", 0, position.character) + 1, 0)
    word_end = line_content.find(" ", position.character)
    if word_end == -1:
        word_end = len(line_content)

    hovered_word = line_content[word_start:word_end].strip()

    print(f"Hovered word: {hovered_word}")

    hover_text = get_hover_content(hovered_word)

    return Hover(contents=hover_text)
