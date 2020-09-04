from commands import ScionCommand
from test.shared.async_mock import AsyncMock

import asyncio
import random
import unittest


class RollCommandTest(unittest.TestCase):
    @unittest.mock.patch('random.randint', return_value=10)
    def test_basic_command(self, mock_randint):
        mock_cmdio = AsyncMock()
        mock_cmdio.message.content = '1'
        command = ScionCommand()
        asyncio.get_event_loop().run_until_complete(command.run(mock_cmdio))

        mock_send = mock_cmdio.message.channel.send
        mock_send.assert_called_once()
        self.assertEqual(mock_send.call_args[0][0], '2 successes! 10')


if __name__ == '__main__':
    unittest.main()
