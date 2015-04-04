import time
import json
import re

TWITCH_STREAMS = "https://api.twitch.tv/kraken/streams/?game="
GAME = "Supreme+Commander:+Forged+Alliance"


class MessageHandler:
    def __init__(self,
                 fetch_url_contents,
                 default_rate_limit_in_seconds=60,
                 per_command_rate_limit_in_seconds=None):

        if not per_command_rate_limit_in_seconds:
            per_command_rate_limit_in_seconds = {}
        self._fetch_url_contents = fetch_url_contents
        self._default_rate_limit = default_rate_limit_in_seconds
        self._per_command_rate_limit = per_command_rate_limit_in_seconds if per_command_rate_limit_in_seconds is not None else {}

        self._command_handlers = {
            'streams': self._get_streams_response,
            'casts': self._get_casts_response
        }

        self._time_of_last_command_usage = {}

    def handle_message(self, message):
        command_name = self._get_command_from_message(message)

        if command_name in self._command_handlers:
            if self._can_get_command_response(command_name):
                return self._get_command_response(command_name, message)

        return []

    def _can_get_command_response(self, command_name):
        if command_name not in self._time_of_last_command_usage:
            return True

        seconds_since_last_execution = time.time() - self._time_of_last_command_usage[command_name]
        rate_limit_in_seconds = self._per_command_rate_limit[command_name] if command_name in self._per_command_rate_limit else self._default_rate_limit

        return seconds_since_last_execution > rate_limit_in_seconds

    def _get_command_response(self, command_name, message):
        self._time_of_last_command_usage[command_name] = time.time()
        return self._command_handlers[command_name](message)

    def _get_command_from_message(self, message):
        message_parts = re.match('!(\w+).*', message)

        if message_parts:
            return message_parts.groups(1)[0]

    def _get_streams_response(self, message):
        responses = []

        streams = json.loads(self._fetch_url_contents(TWITCH_STREAMS + GAME))
        num_of_streams = len(streams["streams"])

        if num_of_streams > 0:
            responses.append("%i Streams online :" % num_of_streams)
            for stream in streams["streams"]:
                t = stream["channel"]["updated_at"]
                date = t.split("T")
                hour = date[1].replace("Z", "")

                responses.append("%s - %s - %s Since %s (%i viewers)" % (
                    stream["channel"]["display_name"], stream["channel"]["status"],
                    stream["channel"]["url"], hour, stream["viewers"]))
        else:
            responses.append("No one is streaming :'(")

        return responses

    def _get_casts_response(self, message):
        responses = []

        info = self._fetch_url_contents(
            "http://gdata.youtube.com/feeds/api/videos?q=forged+alliance+-SWTOR&max-results=5&v=2&orderby=published&alt=jsonc")
        data = json.loads(info)
        responses.append("5 Latest youtube videos:")
        for item in data['data']['items']:
            t = item["uploaded"]
            date = t.split("T")[0]
            like = "0"
            if "likeCount" in item:
                like = item['likeCount']
            responses.append("%s by %s - %s - %s (%s likes) " % (item['title'], item["uploader"],
                                                                 item['player']['default'].replace(
                                                                     "&feature=youtube_gdata_player",
                                                                     ""), date, like))

        return responses
