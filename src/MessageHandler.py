import time
import json
import re

TWITCH_STREAMS = "https://api.twitch.tv/kraken/streams/?game="
GAME = "Supreme+Commander:+Forged+Alliance"


class MessageHandler:

    def __init__(self, fetch_url_contents):
        self.fetch_url_contents = fetch_url_contents

        self.askForCast = 0
        self.askForYoutube = 0

    def handle_message(self, message):
        if message.startswith("!streams"):
            return self._get_streams_response()

        if message.startswith("!casts"):
            return self._get_casts_response()

        return []

    def _get_streams_response(self):
        responses = []

        if time.time() - self.askForCast > 60*10:
            self.askForCast = time.time()

            streams = json.loads(self.fetch_url_contents(TWITCH_STREAMS + GAME))
            num_of_streams = len(streams["streams"])

            if num_of_streams > 0:
                responses.append("%i Streams online :" % num_of_streams)
                for stream in streams["streams"]:
                    t = stream["channel"]["updated_at"]
                    date = t.split("T")
                    hour = date[1].replace("Z", "")

                    responses.append("%s - %s - %s Since %s (%i viewers)" % (stream["channel"]["display_name"], stream["channel"]["status"], stream["channel"]["url"], hour, stream["viewers"]))
            else:
                responses.append("No one is streaming :'(")

        return responses

    def _get_casts_response(self):
        responses = []

        if time.time() - self.askForYoutube > 60*10:
            self.askForYoutube = time.time()
            info = self.fetch_url_contents("http://gdata.youtube.com/feeds/api/videos?q=forged+alliance+-SWTOR&max-results=5&v=2&orderby=published&alt=jsonc")
            data = json.loads(info)
            responses.append("5 Latest youtube videos:")
            for item in data['data']['items']:
                t = item["uploaded"]
                date = t.split("T")[0]
                like = "0"
                if "likeCount" in item:
                    like = item['likeCount']
                responses.append("%s by %s - %s - %s (%s likes) " % (item['title'], item["uploader"], item['player']['default'].replace("&feature=youtube_gdata_player", ""), date, like))

        return responses
