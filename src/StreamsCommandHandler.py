import json


class StreamsCommandHandler:
    def __init__(self, url_content_fetcher):
        self._fetch_url_contents = url_content_fetcher

        self._TWITCH_URL = "https://api.twitch.tv/kraken/streams/?game="
        self._GAME_NAME = "Supreme+Commander:+Forged+Alliance"

    def get_response_for(self, message):
        responses = []

        streams = json.loads(self._fetch_url_contents(self._TWITCH_URL + self._GAME_NAME))
        num_of_streams = len(streams["streams"])

        if num_of_streams > 0:
            responses.append("%i Streams online :" % num_of_streams)

            for stream in streams["streams"]:
                responses.append(self._get_stream_line(stream))
        else:
            responses.append("No one is streaming :'(")

        return responses

    def _get_stream_line(self, stream):
        t = stream["channel"]["updated_at"]
        date = t.split("T")
        hour = date[1].replace("Z", "")

        return "%s - %s - %s Since %s (%i viewers)" % \
            (
                stream["channel"]["display_name"],
                stream["channel"]["status"],
                stream["channel"]["url"],
                hour,
                stream["viewers"]
            )
