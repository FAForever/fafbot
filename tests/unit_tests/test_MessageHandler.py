from src.MessageHandler import MessageHandler


def test_given_unknown_command__empty_list_is_returned():
    assert MessageHandler().handle_message('!unknown') == []


def test_given_known_command__command_result_is_returned():
    assert MessageHandler().handle_message('!nyan') == ['~=[,,_,,]:3']
