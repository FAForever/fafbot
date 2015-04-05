from src.MessageHandlerBuilder import MessageHandlerBuilder


def test_given_unknown_command__empty_list_is_returned():
    assert MessageHandlerBuilder({}).new_message_handler()('!unknown') == []


def test_given_known_command__command_result_is_returned():
    assert MessageHandlerBuilder({}).new_message_handler()('!nyan') == ['~=[,,_,,]:3']


def test_default_rate_limit_option_is_acted_upon():
    message_handler = MessageHandlerBuilder({'default_rate_limit': "0"}).new_message_handler()

    message_handler('!nyan')
    assert message_handler('!nyan') == ['~=[,,_,,]:3']
