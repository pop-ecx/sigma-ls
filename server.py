# The journey of a thousand miles
from language_server import LanguageServer

server = LanguageServer()

@server.command('initialize')
def initialize(params):
    return {
        'capabilities': {
            'textDocument': {
                'formatting': {
                    'dynamicRegistration': True
                }
            }
        }
    }


server.start_io()
