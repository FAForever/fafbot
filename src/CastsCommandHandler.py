import json


class CastsCommandHandler:
    def __init__(self, url_content_fetcher):
        self._fetch_url_contents = url_content_fetcher

        self._CASTS_URL = "http://gdata.youtube.com/feeds/api/videos?q=forged+alliance+-SWTOR&max-results=5&v=2&orderby=published&alt=jsonc"

    def get_response_for(self, message):
        responses = []

        data = json.loads(self._fetch_url_contents(self._CASTS_URL))
        responses.append("5 Latest youtube videos:")

        for video in data['data']['items']:
            responses.append(self._get_cast_line(video))

        return responses

    def _get_cast_line(self, video):
        date = video["uploaded"].split("T")[0]

        like_count = video['likeCount'] if 'likeCount' in video else "0"

        return "%s by %s - %s - %s (%s likes)" % \
        (
            video['title'],
            video["uploader"],
            video['player']['default'].replace("&feature=youtube_gdata_player", ""),
            date,
            like_count
        )
