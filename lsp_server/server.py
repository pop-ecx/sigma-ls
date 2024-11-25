from pygls.server import LanguageServer

class SigmaLanguageServer(LanguageServer):
    def __init__(self):
        super().__init__("Sigma-ls", "v0.1")

