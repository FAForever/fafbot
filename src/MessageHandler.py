import json
import urllib2
from src.MessageRouter import MessageRouter


def new_message_handler(config):
    def _new_command_handlers():
        return {
            'casts': _new_casts_handler(),
            'streams': new_get_streams_response(fetch_url_contents),
            'nyan': lambda message: ['~=[,,_,,]:3']
        }

    def _new_casts_handler():
        return new_get_cats_response(
            get_url_contents=fetch_url_contents,
            blacklisted_youtubers=config['blacklisted_youtubers'] if 'blacklisted_youtubers' in config else [],
            cast_count=int(config['cast_count']) if 'cast_count' in config else 5
        )

    message_router = MessageRouter(
        command_handlers=_new_command_handlers(),
        default_rate_limit_in_seconds=int(config['default_rate_limit']) if 'default_rate_limit' in config else 60
    )

    return message_router.handle_message


def new_get_cats_response(get_url_contents, blacklisted_youtubers=[], cast_count=5):
    def _get_videos_from_data(data):
        return filter(_can_use_video, data['data']['items'])[:cast_count]

    def _can_use_video(video):
        return not _youtuber_is_blacklisted(video["uploader"])

    def _youtuber_is_blacklisted(youtuber):
        return youtuber in blacklisted_youtubers

    def _get_cast_line(video):
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

    def get_cats_response(message):
        cats_url = "http://gdata.youtube.com/feeds/api/videos?" \
                   + "q=forged+alliance+-SWTOR&max-results=%s&v=2&orderby=published&alt=jsonc" % cast_count * 2

        responses = ["%s Latest youtube videos:" % cast_count]

        data = json.loads(get_url_contents(cats_url))

        for video in _get_videos_from_data(data):
            responses.append(_get_cast_line(video))

        return responses

    return get_cats_response


def new_get_streams_response(get_url_contents):

    def _get_stream_line(stream):
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

    def get_streams_response(message):
        twitch_url = "https://api.twitch.tv/kraken/streams/?game="
        game_name = "Supreme+Commander:+Forged+Alliance"

        responses = []

        streams = json.loads(get_url_contents(twitch_url + game_name))
        num_of_streams = len(streams["streams"])

        if num_of_streams > 0:
            responses.append("%i Streams online :" % num_of_streams)

            for stream in streams["streams"]:
                responses.append(_get_stream_line(stream))
        else:
            responses.append("No one is streaming :'(")

        return responses

    return get_streams_response


def fetch_url_contents(url):
    con = urllib2.urlopen(url)
    response = con.read()
    con.close()

    return response
