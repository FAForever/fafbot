from src.StreamsCommandHandler import StreamsCommandHandler


def new_url_content_fetcher(file_name):
    return lambda url: open('tests/data/' + file_name, 'r').read()


def test_when_no_one_is_streaming__streams_command_returns_sadface():
    message_handler = StreamsCommandHandler(new_url_content_fetcher('twitch-streams-none.json'))

    assert message_handler.get_response_for('!streams') == ["No one is streaming :'("]


def test_when_one_person_is_streaming__streams_command_returns_steam_count_1_and_stream():
    message_handler = StreamsCommandHandler(new_url_content_fetcher('twitch-streams-one.json'))

    assert message_handler.get_response_for('!streams') == [
        "1 Streams online :",
        "TAG_Chosen - THERE YOU GO - http://www.twitch.tv/tag_chosen Since 15:52:44 (3 viewers)"
    ]


def test_when_two_people_are_streaming__streams_command_returns_both_streams():
    message_handler = StreamsCommandHandler(new_url_content_fetcher('twitch-streams-two.json'))

    assert message_handler.get_response_for('!streams') == [
        "2 Streams online :",
        "zockyzock - BO50 vs petric winner gets tiep nudes - http://www.twitch.tv/zockyzock Since 17:21:06 (10 viewers)",
        "TAG_Chosen - THERE YOU GO - http://www.twitch.tv/tag_chosen Since 17:16:06 (5 viewers)"
    ]
