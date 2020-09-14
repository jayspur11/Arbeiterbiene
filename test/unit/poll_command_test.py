import asyncio
import commands
import unittest

from test.shared import async_mock
from unittest import mock


class PollCommandTest(unittest.TestCase):
    def test_basic_command(self):
        command = commands.PollCommand()
        mock_cmdio = async_mock.AsyncMock()
        mock_cmdio.message.content = "<:name:customID> 💩"
        mock_custemo = mock.Mock(id='customID')
        mock_cmdio.message.guild.emojis = [mock_custemo]

        asyncio.get_event_loop().run_until_complete(command.run(mock_cmdio))

        mock_react = mock_cmdio.message.add_reaction
        mock_react.assert_has_calls([mock.call(mock_custemo), mock.call("💩")])


if __name__ == '__main__':
    unittest.main()
