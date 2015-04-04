from fafbot import BotModeration

def test_given_unknown_command__handle_message_returns_empty_list():
    assert BotModeration().handle_message('!nyan') == []

def test_when_no_one_is_streaming__streams_command_returns_sadface():
    bot = BotModeration()
    bot.url_content_fetcher = lambda url: open('tests/data/twitch-streams-none.json', 'r').read()

    assert bot.handle_message('!streams') == ["No one is streaming :'("]

def test_when_one_person_is_streaming__streams_command_returns_steam_count_1_and_stream():
    bot = BotModeration()
    bot.url_content_fetcher = lambda url: open('tests/data/twitch-streams-one.json', 'r').read()

    assert bot.handle_message('!streams') == ["1 Streams online :", "TAG_Chosen - THERE YOU GO - http://www.twitch.tv/tag_chosen Since 15:52:44 (3 viewers)"]
