from commands import MeowCommand
from test.shared.async_mock import AsyncMock

import asyncio
import json
import urllib
import unittest


class MeowCommandTest(unittest.TestCase):
    @unittest.mock.patch('json.loads')
    @unittest.mock.patch('urllib.request.urlopen')
    def test_basic_command(self, mock_urlopen, mock_loads):
        mock_urlopen.__enter__ = unittest.mock.Mock(return_value=(unittest.mock.Mock(), None))
        mock_urlopen.__exit__ = unittest.mock.Mock(return_value=None)
        mock_loads.return_value = {'fact': 'funfact', 'link': 'linkurl'}
        mock_cmdio = AsyncMock()
        command = MeowCommand()
        asyncio.get_event_loop().run_until_complete(command.run(mock_cmdio))

        mock_send = mock_cmdio.message.channel.send
        mock_send.assert_called_once()
        self.assertEqual(mock_send.call_args[0], ('funfact',))
        self.assertEqual(mock_send.call_args[1]['embed'].image.url, 'linkurl')


if __name__ == '__main__':
    unittest.main()
