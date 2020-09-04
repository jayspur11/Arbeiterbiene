from commands import DieCommand
from test.shared.async_mock import AsyncMock

import asyncio
import unittest


class DieCommandTest(unittest.TestCase):
    def test_basic_command(self):
        command = DieCommand()
        mock_cmdio = AsyncMock()
        with self.assertRaises(KeyboardInterrupt):
            asyncio.get_event_loop().run_until_complete(command.run(mock_cmdio))


if __name__ == '__main__':
    unittest.main()
