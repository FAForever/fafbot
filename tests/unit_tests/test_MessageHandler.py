from src.MessageHandler import MessageHandler


def test_given_unknown_command__empty_list_is_returned():
    message_handler = MessageHandler(new_url_content_fetcher('twitch-streams-none.json'))
    assert message_handler.handle_message('!nyan') == []


def new_url_content_fetcher(file_name):
    return lambda url: open('tests/data/' + file_name, 'r').read()


def test_when_no_one_is_streaming__streams_command_returns_sadface():
    message_handler = MessageHandler(new_url_content_fetcher('twitch-streams-none.json'))

    assert message_handler.handle_message('!streams') == ["No one is streaming :'("]


def test_when_one_person_is_streaming__streams_command_returns_steam_count_1_and_stream():
    message_handler = MessageHandler(new_url_content_fetcher('twitch-streams-one.json'))

    assert message_handler.handle_message('!streams') == ["1 Streams online :",
                                                          "TAG_Chosen - THERE YOU GO - http://www.twitch.tv/tag_chosen Since 15:52:44 (3 viewers)"]
