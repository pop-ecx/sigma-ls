"""
Completions feature
"""
from lsprotocol.types import (
    TEXT_DOCUMENT_COMPLETION,
    CompletionItem,
    CompletionItemKind,
    CompletionParams,
    InsertTextFormat,
)

def register_completion_feature(server):
    """Register the completion feature with the LSP server"""

    @server.feature(TEXT_DOCUMENT_COMPLETION)
    def completion(params: CompletionParams):
        # Provide completion suggestions for Sigma rules.
        completions = [
            CompletionItem(
                label="title",
                kind=CompletionItemKind.Keyword,
                detail="Define the rule title",
                insert_text="title: ${1:Rule Title}",
                insert_text_format=InsertTextFormat.Snippet,
            ),
            CompletionItem(
                label="logsource",
                kind=CompletionItemKind.Keyword,
                detail="Define the logsource details",
                insert_text="logsource:\n  category: ${1:category}\n  product: ${2:product}",
                insert_text_format=InsertTextFormat.Snippet,
            ),
            CompletionItem(
                label="detection",
                kind=CompletionItemKind.Keyword,
                detail="Define the detection criteria",
                insert_text=(
                    "detection:\n"
                    "  selection:\n"
                    "    ${1:field_name}: ${2:value}\n"
                    "  condition: ${3:selection}"
                ),
                insert_text_format=InsertTextFormat.Snippet,
            ),
            CompletionItem(
                label="condition",
                kind=CompletionItemKind.Keyword,
                detail="Define the condition for detection",
                insert_text="condition: ${1:condition}",
                insert_text_format=InsertTextFormat.Snippet,
            ),
            CompletionItem(
                label="author",
                kind=CompletionItemKind.Keyword,
                detail="Define the author",
                insert_text="author: ${1:Author Name}",
                insert_text_format=InsertTextFormat.Snippet,
            ),
            CompletionItem(
                label="id",
                kind=CompletionItemKind.Keyword,
                detail="Provide a unique identifier for the rule",
                insert_text="id: ${1:unique-id}",
                insert_text_format=InsertTextFormat.Snippet,
            ),
            CompletionItem(
                label="status",
                kind=CompletionItemKind.Keyword,
                detail="Define the rule's status",
                insert_text="status: ${1:stable|experimental|deprecated}",
                insert_text_format=InsertTextFormat.Snippet,
            ),
            CompletionItem(
                label="description",
                kind=CompletionItemKind.Keyword,
                detail="Describe the rule's purpose",
                insert_text="description: ${1:Description of the rule}",
                insert_text_format=InsertTextFormat.Snippet,
            ),
            CompletionItem(
                label="falsepositives",
                kind=CompletionItemKind.Keyword,
                detail="Define known false positives",
                insert_text="falsepositives:\n  - ${1:example}",
                insert_text_format=InsertTextFormat.Snippet,
            ),
            CompletionItem(
                label="level",
                kind=CompletionItemKind.Keyword,
                detail="Define the severity level",
                insert_text="level: ${1:low|medium|high|critical}",
                insert_text_format=InsertTextFormat.Snippet,
            ),
            CompletionItem(
                label="CommandLine|contains",
                kind=CompletionItemKind.Keyword,
                detail="Define what commandline contains in your selection",
                insert_text="CommandLine|contains:\n  - ${1:bash -c}\n  - ${2:iex}",
                insert_text_format=InsertTextFormat.Snippet,
            ),
            CompletionItem(
                label="Tags",
                kind=CompletionItemKind.Keyword,
                detail="Reference MITRE ATT&CK, CAR, TLP or CVE ",
                insert_text="tags:\n  - ${1:attack.t1012}\n  - ${2:cve.2023-27997}",
                insert_text_format=InsertTextFormat.Snippet,
            ),
        ]

        return completions
