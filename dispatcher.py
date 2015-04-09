from functools import wraps
import json
import urllib2
import re
import time


def is_irc_callback(param):
    return callable(param) and hasattr(param, 'irc_format')


def irc_command(format='', limit=1):
    def wrapper(f):
        @wraps(f)
        def _(*args, **kwargs):
            f(*args, **kwargs)
        _.irc_format = format
        _.limit = limit
        return _
    return wrapper


def dispatcher(*args, **kwargs):
    """
    Make a dispatcher object for irc-messages,
    given classes to look for marked functions as targets
    """
    target_callbacks = []
    for target in args:
        target_callbacks.append({name: getattr(target, name)
                                 for name in dir(target)
                                 if is_irc_callback(getattr(target, name))})
    call_times = {cb: 0 for target in target_callbacks
                        for name, cb in target.items()}
    def dispatch(msg='', source='', channel=''):
        for target in target_callbacks:
            for name, cb in target.items():
                m = re.match(cb.irc_format, msg)
                if m and time.time() - call_times[cb] > cb.limit:
                    # TODO: Get fancy and inspect funcargs
                    # to only pass what it requests
                    # Pass named regex groups as kwargs?
                    cb(msg, source, channel, m.groups())
                    call_times[cb] = time.time()
    return dispatch


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
