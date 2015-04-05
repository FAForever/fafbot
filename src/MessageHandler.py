import urllib2
from src.CastsCommandHandler import CastsCommandHandler
from src.MessageRouter import MessageRouter
from src.StreamsCommandHandler import StreamsCommandHandler


class MessageHandler:
    """
    This class is responsible for constructing the object graph needed
    to handle messages and to delegate to it.
    """

    def __init__(self, config):
        casts_handler = CastsCommandHandler(
            url_content_fetcher=fetch_url_contents,
            blacklisted_youtubers=config['blacklisted_youtubers'] if 'blacklisted_youtubers' in config else [],
            cast_count=int(config['cast_count']) if 'cast_count' in config else 5
        )

        command_handlers = {
            'casts': casts_handler.get_response_for,
            'streams': StreamsCommandHandler(fetch_url_contents).get_response_for,
            'nyan': lambda message: ['~=[,,_,,]:3']
        }

        self._message_router = MessageRouter(
            command_handlers=command_handlers,
            default_rate_limit_in_seconds=int(config['default_rate_limit']) if 'default_rate_limit' in config else 60
        )

    def handle_message(self, message):
        return self._message_router.handle_message(message)


def fetch_url_contents(url):
    con = urllib2.urlopen(url)
    response = con.read()
    con.close()

    return response
