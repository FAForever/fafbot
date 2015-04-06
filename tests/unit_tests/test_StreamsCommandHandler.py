from src.MessageHandler import new_get_streams_response


def new_url_content_fetcher(file_name):
    return lambda url: open('tests/data/' + file_name, 'r').read()


def test_when_no_one_is_streaming__streams_command_returns_sadface():
    get_streams_response = new_get_streams_response(new_url_content_fetcher('twitch-streams-none.json'))

    assert get_streams_response('!streams') == ["No one is streaming :'("]


def test_when_one_person_is_streaming__streams_command_returns_steam_count_1_and_stream():
    get_streams_response = new_get_streams_response(new_url_content_fetcher('twitch-streams-one.json'))

    assert get_streams_response('!streams') == [
        "1 Streams online :",
        "TAG_Chosen - THERE YOU GO - http://www.twitch.tv/tag_chosen Since 15:52:44 (3 viewers)"
    ]


def test_when_two_people_are_streaming__streams_command_returns_both_streams():
    get_streams_response = new_get_streams_response(new_url_content_fetcher('twitch-streams-two.json'))

    assert get_streams_response('!streams') == [
        "2 Streams online :",
        "zockyzock - BO50 vs petric winner gets tiep nudes - http://www.twitch.tv/zockyzock Since 17:21:06 (10 viewers)",
        "TAG_Chosen - THERE YOU GO - http://www.twitch.tv/tag_chosen Since 17:16:06 (5 viewers)"
    ]
