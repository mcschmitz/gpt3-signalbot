# flake8: noqa
from unittest.mock import patch

from signalbot.utils import ChatTestCase, chat

from commands.gpt3 import GPT3Command


class MockedChoice:
    def __init__(self) -> None:
        self.text = "test_result  "


class MockedCompletionResult:
    def __init__(self) -> None:
        self.choices = [MockedChoice()]


class GPT3CommandTest(ChatTestCase):
    def setUp(self):
        super().setUp()
        self.signal_bot.register(GPT3Command())

    @patch("signalbot.context.Context.start_typing", return_value=None)
    @patch("signalbot.context.Context.stop_typing", return_value=None)
    @patch("openai.Completion.create", return_value=MockedCompletionResult())
    @chat("Hey this is a test")
    def test_gpt3_command(
        self,
        query,
        replies,
        reactions,
        mocked_type_start,
        mocked_type_stop,
        mocked_completion_result,
    ):
        self.assertEqual(replies.call_count, 1)
        for recipient, message in replies.results():
            self.assertEqual(recipient, ChatTestCase.group_secret)
            self.assertEqual(message, "test_result")
