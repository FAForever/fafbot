import json


class CastsCommandHandler:
    def __init__(self, url_content_fetcher, blacklisted_youtubers=None, cast_count=5):
        self._fetch_url_contents = url_content_fetcher
        self._blacklisted_youtubers = blacklisted_youtubers if blacklisted_youtubers is not None else []
        self._cast_count = cast_count

        self._CASTS_URL = "http://gdata.youtube.com/feeds/api/videos?" \
                          + "q=forged+alliance+-SWTOR&max-results=%s&v=2&orderby=published&alt=jsonc" % self._cast_count * 2

    def get_response_for(self, message):
        responses = ["%s Latest youtube videos:" % self._cast_count]

        data = json.loads(self._fetch_url_contents(self._CASTS_URL))

        for video in self._get_videos_from_data(data):
            responses.append(self._get_cast_line(video))

        return responses

    def _get_videos_from_data(self, data):
        return filter(self._can_use_video, data['data']['items'])[:self._cast_count]

    def _can_use_video(self, video):
        return not self._youtuber_is_blacklisted(video["uploader"])

    def _youtuber_is_blacklisted(self, youtuber):
        return youtuber in self._blacklisted_youtubers

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
