from fafbot import BotModeration

def test_given_unknown_command__handle_message_returns_empty_list():
    assert BotModeration().handle_message('!nyan') == []

def test_when_no_one_is_streaming__streams_command_returns_sadface():
    bot = BotModeration()
    bot.url_content_fetcher = lambda url: open('tests/data/twitch-streams-none.json', 'r').read()

    assert bot.handle_message('!streams') == ["No one is streaming :'("]
