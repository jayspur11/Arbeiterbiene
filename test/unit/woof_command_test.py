import asyncio
import commands
import json
import urllib
import unittest

from test.shared import async_mock
from unittest import mock


class WoofCommandTest(unittest.TestCase):
    @mock.patch('json.loads')
    @mock.patch('urllib.request.urlopen')
    def test_basic_command(self, mock_urlopen, mock_loads):
        mock_urlopen.__enter__ = mock.Mock(return_value=(mock.Mock(), None))
        mock_urlopen.__exit__ = mock.Mock(return_value=None)
        mock_loads.return_value = {'fact': 'funfact', 'link': 'linkurl'}
        mock_cmdio = async_mock.AsyncMock()
        command = commands.WoofCommand()
        asyncio.get_event_loop().run_until_complete(command.run(mock_cmdio))

        mock_send = mock_cmdio.message.channel.send
        mock_send.assert_called_once()
        self.assertEqual(mock_send.call_args[0], ('funfact', ))
        self.assertEqual(mock_send.call_args[1]['embed'].image.url, 'linkurl')


if __name__ == '__main__':
    unittest.main()
