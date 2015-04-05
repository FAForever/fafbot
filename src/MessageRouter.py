import time
import re


class MessageRouter:
    """
    Responsible for invoking a message command handler if a message contains
    a command and the rate limit is not exceeded.
    """

    def __init__(self,
                 command_handlers=None,
                 default_rate_limit_in_seconds=60,
                 per_command_rate_limit_in_seconds=None):

        if not per_command_rate_limit_in_seconds:
            per_command_rate_limit_in_seconds = {}
        self._default_rate_limit = default_rate_limit_in_seconds
        self._command_handlers = command_handlers if command_handlers is not None else {}
        self._per_command_rate_limit = per_command_rate_limit_in_seconds if per_command_rate_limit_in_seconds is not None else {}

        self._time_of_last_command_usage = {}

    def handle_message(self, message):
        command_name = self._get_command_from_message(message)

        if command_name in self._command_handlers:
            if self._can_get_command_response(command_name):
                return self._get_command_response(command_name, message)

        return []

    def _can_get_command_response(self, command_name):
        if command_name not in self._time_of_last_command_usage:
            return True

        seconds_since_last_execution = time.time() - self._time_of_last_command_usage[command_name]
        rate_limit_in_seconds = self._per_command_rate_limit[command_name] if command_name in self._per_command_rate_limit else self._default_rate_limit

        return seconds_since_last_execution > rate_limit_in_seconds

    def _get_command_response(self, command_name, message):
        self._time_of_last_command_usage[command_name] = time.time()
        return self._command_handlers[command_name](message)

    def _get_command_from_message(self, message):
        message_parts = re.match('!(\w+).*', message)

        if message_parts:
            return message_parts.groups(1)[0]
