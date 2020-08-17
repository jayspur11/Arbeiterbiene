from commands import PollCommand
from test.shared.async_mock import AsyncMock

import asyncio
import unittest


class PollCommandTest(unittest.TestCase):
    def test_basic_command(self):
        command = PollCommand()
        mock_cmdio = AsyncMock()
        mock_cmdio.message.content = "<:name:customID> 💩"
        mock_custemo = unittest.mock.Mock(id='customID')
        mock_cmdio.message.guild.emojis = [mock_custemo]

        asyncio.get_event_loop().run_until_complete(command.run(mock_cmdio))

        mock_react = mock_cmdio.message.add_reaction
        mock_react.assert_has_calls(
            [unittest.mock.call(mock_custemo),
             unittest.mock.call("💩")])


if __name__ == '__main__':
    unittest.main()
