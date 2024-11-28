from lsprotocol.types import TEXT_DOCUMENT_COMPLETION, CompletionItem, CompletionItemKind, CompletionParams

def register_completion_feature(server):
    #Register the completion feature with the LSP server.

    @server.feature(TEXT_DOCUMENT_COMPLETION)
    def completion(params: CompletionParams):
        #Provide completion suggestions for Sigma rules.
        completions = [
            CompletionItem(
                label="title",
                kind=CompletionItemKind.Keyword,
                detail="Define the rule title",
                insert_text="title: ",
            ),
            CompletionItem(
                label="logsource",
                kind=CompletionItemKind.Keyword,
                detail="Define the logsource details",
                insert_text="logsource:\n  category: \n  product: ",
            ),
            CompletionItem(
                label="detection",
                kind=CompletionItemKind.Keyword,
                detail="Define the detection criteria",
                insert_text="detection:\n  selection:\n    field_name: value\n  condition: selection",
            ),
            CompletionItem(
                label="condition",
                kind=CompletionItemKind.Keyword,
                detail="Define the condition for detection",
                insert_text="condition: ",
            ),
        ]

        return completions
