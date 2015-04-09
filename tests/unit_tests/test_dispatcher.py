import mock

from dispatcher import dispatcher, irc_command


def test_dispatch_all():
    m = mock.Mock()
    class TestClass(object):
        @irc_command(format='.*')
        def on_anything(self, msg, source, channel, groups):
            print("Called with {}".format(msg))
            m()
    test = TestClass()
    d = dispatcher(test)
    d(msg='Test', source='Some_Guy', channel='#aeolus')
    m.assert_any_call()


def test_dispatch_word_group():
    m = mock.Mock()
    class TestClass(object):
        @irc_command(format='!(\w+).*')
        def on_word(self, msg, source, channel, groups):
            m(msg, source, channel, groups)
    test = TestClass()
    d = dispatcher(test)
    d(msg='!help', source='Some_Guy', channel='#aeolus')
    m.assert_called_with('!help', 'Some_Guy', '#aeolus', ('help',))


def test_dispatch_rate_limit():
    m = mock.Mock()
    class TestClass(object):
        @irc_command(format='.*', limit=5)
        def on_word(self, msg, source, channel, groups):
            m(msg, source, channel, groups)
    test = TestClass()
    d = dispatcher(test)
    d(msg='1', source='Some_Guy', channel='#aeolus')
    d(msg='2', source='Some_Guy', channel='#aeolus')
    assert m.mock_calls == [mock.call('1', 'Some_Guy', '#aeolus', ())]
