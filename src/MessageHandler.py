import urllib2
from src.CastsCommandHandler import CastsCommandHandler
from src.MessageRouter import MessageRouter
from src.StreamsCommandHandler import StreamsCommandHandler


class MessageHandler:
    """
    This class is responsible for constructing the object graph needed
    to handle messages and to delegate to it.
    """

    def __init__(self):
        self._fetch_url_contents = fetch_url_contents

        command_handlers = {
            'streams': StreamsCommandHandler(fetch_url_contents).get_response_for,
            'casts': CastsCommandHandler(fetch_url_contents).get_response_for,
            'nyan': lambda message: ['~=[,,_,,]:3']
        }

        self._message_router = MessageRouter(command_handlers=command_handlers)

    def handle_message(self, message):
        return self._message_router.handle_message(message)


def fetch_url_contents(url):
    con = urllib2.urlopen(url)
    response = con.read()
    con.close()

    return response






