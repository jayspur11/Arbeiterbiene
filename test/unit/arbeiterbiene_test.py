import arbeiterbiene
import discord
import unittest

from test.shared import async_mock
from unittest import mock


class ArbeiterbieneTest(unittest.TestCase):
    def setUp(self):
        self._mock_command = async_mock.AsyncMock()
        self._patches = {
            'registry':
            mock.patch('commands.command_registry',
                       return_value={'command': self._mock_command})
        }
        self._mocks = {}
        for k in self._patches:
            self._mocks[k] = self._patches[k].start()

    def tearDown(self):
        for patch in self._patches.values():
            patch.stop()

    def test_command_called_in_dm(self):
        bot = arbeiterbiene.Arbeiterbiene('', '')
        message = mock.Mock()
        message.content = '@bot command argument1 argument2'
        message.channel.mock_add_spec(discord.DMChannel)

        bot.loop.run_until_complete(bot.on_message(message))

        self._mock_command.run.assert_called_once()

    def test_command_called_in_group(self):
        bot = arbeiterbiene.Arbeiterbiene('', '')
        message = mock.Mock()
        message.content = '@bot command argument1 argument2'
        message.channel.mock_add_spec(discord.GroupChannel)

        bot.loop.run_until_complete(bot.on_message(message))

        self._mock_command.run.assert_called_once()

    def test_command_called_when_mentioned(self):
        bot = arbeiterbiene.Arbeiterbiene('', '')
        _mock_user = mock.patch.object(arbeiterbiene.Arbeiterbiene,
                                       'user',
                                       id=123).start()
        message = mock.Mock(raw_mentions=[123])
        message.content = '@bot command argument1 argument2'

        bot.loop.run_until_complete(bot.on_message(message))

        self._mock_command.run.assert_called_once()

    def test_message_content_pruned(self):
        bot = arbeiterbiene.Arbeiterbiene('', '')
        message = mock.Mock()
        message.content = '@bot command argument1 argument2'
        message.channel.mock_add_spec(discord.DMChannel)

        bot.loop.run_until_complete(bot.on_message(message))

        self.assertEqual(message.content, 'argument1 argument2')


if __name__ == "__main__":
    unittest.main()
