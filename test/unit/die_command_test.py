import asyncio
import commands
import unittest

from test.shared import async_mock


class DieCommandTest(unittest.TestCase):
    def test_basic_command(self):
        command = commands.DieCommand()
        mock_cmdio = async_mock.AsyncMock()
        with self.assertRaises(KeyboardInterrupt):
            asyncio.get_event_loop().run_until_complete(
                command.run(mock_cmdio))


if __name__ == '__main__':
    unittest.main()
