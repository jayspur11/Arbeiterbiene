from commands import RollCommand
from test.shared.async_mock import AsyncMock

import asyncio
import random
import unittest


class RollCommandTest(unittest.TestCase):
    @unittest.mock.patch('random.randint', return_value=20)
    def test_basic_command(self, mock_randint):
        mock_cmdio = AsyncMock()
        mock_cmdio.message.content = '1d20'
        command = RollCommand()
        asyncio.get_event_loop().run_until_complete(command.run(mock_cmdio))

        mock_send = mock_cmdio.message.channel.send
        mock_send.assert_called_once()
        self.assertEqual(mock_send.call_args[0][0], '**20**\n(20)')


if __name__ == '__main__':
    unittest.main()
