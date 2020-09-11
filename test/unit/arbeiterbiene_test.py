from arbeiterbiene import Arbeiterbiene
from test.shared.async_mock import AsyncMock
from unittest.mock import Mock
from unittest.mock import patch

import discord
import unittest


class ArbeiterbieneTest(unittest.TestCase):
    def setUp(self):
        self._mock_command = AsyncMock()
        self._patches = {
            'registry':
            patch('commands.command_registry',
                  return_value={'command': self._mock_command})
        }
        self._mocks = {}
        for k in self._patches:
            self._mocks[k] = self._patches[k].start()

    def tearDown(self):
        for patch in self._patches.values():
            patch.stop()

    def test_command_called_in_dm(self):
        bot = Arbeiterbiene('')
        message = Mock()
        message.content = '@bot command argument1 argument2'
        message.channel.mock_add_spec(discord.DMChannel)

        bot.loop.run_until_complete(bot.on_message(message))

        self._mock_command.run.assert_called_once()

    def test_command_called_in_group(self):
        bot = Arbeiterbiene('')
        message = Mock()
        message.content = '@bot command argument1 argument2'
        message.channel.mock_add_spec(discord.GroupChannel)

        bot.loop.run_until_complete(bot.on_message(message))

        self._mock_command.run.assert_called_once()

if __name__ == "__main__":
    unittest.main()
