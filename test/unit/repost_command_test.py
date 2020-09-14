import asyncio
import commands
import random
import unittest

from test.shared import async_mock
from unittest import mock


class RepostCommandTest(unittest.TestCase):
    def setUp(self):
        self._patches = {
            'datetime': mock.patch('commands.repost_command.datetime'),
            'randint': mock.patch('random.randint', return_value=2)
        }
        self._mocks = {}
        for k in self._patches:
            self._mocks[k] = self._patches[k].start()

        self._mocks['datetime'].now().time().hour = 12

    def tearDown(self):
        for patch in self._patches.values():
            patch.stop()

    def test_basic_command(self):
        mock_cmdio = async_mock.AsyncMock(send=lambda: None)
        mock_cmdio.message.attachments = [mock.Mock(url='fakeURL')]
        command = commands.RepostCommand()
        asyncio.get_event_loop().run_until_complete(command.run(mock_cmdio))
        asyncio.get_event_loop().run_until_complete(asyncio.sleep(3))

        mock_send = mock_cmdio.message.channel.send
        mock_send.assert_called_once()
        self.assertEqual(mock_send.call_args[1]['embed'].image.url, 'fakeURL')


if __name__ == '__main__':
    unittest.main()
