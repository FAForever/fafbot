from src.MessageRouter import MessageRouter


def test_given_unknown_command__empty_list_is_returned():
    assert MessageRouter().handle_message('!unknown') == []


def new_nyan_command_handlers():
    return {'nyan': lambda message: ['~=[,,_,,]:3']}


def new_nyan_router():
    return MessageRouter(command_handlers=new_nyan_command_handlers())


def test_given_known_command__command_result_is_returned():
    assert new_nyan_router().handle_message('!nyan') == ['~=[,,_,,]:3']


def test_given_known_command_with_arguments__command_result_is_returned():
    assert new_nyan_router().handle_message('!nyan foo bar baz') == ['~=[,,_,,]:3']


def test_immediate_repeat_of_command_leads_to_empty_result():
    router = new_nyan_router()

    router.handle_message('!nyan')
    assert router.handle_message('!nyan') == []


def test_when_rate_limit_is_zero__immediate_repeat_of_command_returns_same_result():
    router = MessageRouter(
        command_handlers=new_nyan_command_handlers(),
        default_rate_limit_in_seconds=0
    )

    router.handle_message('!nyan')
    assert router.handle_message('!nyan') == ['~=[,,_,,]:3']


def test_command_specific_rate_limit_overrides_the_default():
    router = MessageRouter(
        command_handlers=new_nyan_command_handlers(),
        per_command_rate_limit_in_seconds={'nyan': 0}
    )

    router.handle_message('!nyan')
    assert router.handle_message('!nyan') == ['~=[,,_,,]:3']
