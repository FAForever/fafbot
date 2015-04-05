import urllib2
from src.CastsCommandHandler import CastsCommandHandler
from src.MessageRouter import MessageRouter
from src.StreamsCommandHandler import StreamsCommandHandler


class MessageHandlerBuilder:
    """
    This class is responsible for constructing the object graph needed to handle messages.
    """

    def __init__(self, config):
        self._config = config

    def new_message_handler(self):
        message_router = MessageRouter(
            command_handlers=self._new_command_handlers(),
            default_rate_limit_in_seconds=int(self._config['default_rate_limit']) if 'default_rate_limit' in self._config else 60
        )

        return message_router.handle_message

    def _new_command_handlers(self):
        return {
            'casts': self._new_casts_handler().get_response_for,
            'streams': StreamsCommandHandler(fetch_url_contents).get_response_for,
            'nyan': lambda message: ['~=[,,_,,]:3']
        }

    def _new_casts_handler(self):
        return CastsCommandHandler(
            url_content_fetcher=fetch_url_contents,
            blacklisted_youtubers=self._config['blacklisted_youtubers'] if 'blacklisted_youtubers' in self._config else [],
            cast_count=int(self._config['cast_count']) if 'cast_count' in self._config else 5
        )


def fetch_url_contents(url):
    con = urllib2.urlopen(url)
    response = con.read()
    con.close()

    return response
