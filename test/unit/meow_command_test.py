import asyncio
import commands
import json
import urllib
import unittest

from test.shared import async_mock
from unittest import mock


def urlopen_mocked(req):
    mock_response = mock.Mock()
    if "img" in req.full_url:
        mock_response.read.return_value = b"""
            {
                "link": "linkurl"
            }
        """
    elif "fact" in req.full_url:
        mock_response.read.return_value = b"""
            {
                "fact": "funfact"
            }
        """

    mock_context_manager = mock.MagicMock()
    mock_context_manager.__enter__.return_value = mock_response
    return mock_context_manager


class MeowCommandTest(unittest.TestCase):
    @mock.patch('urllib.request.urlopen', side_effect=urlopen_mocked)
    def test_basic_command(self, mock_urlopen):
        mock_cmdio = async_mock.AsyncMock()
        command = commands.MeowCommand()
        asyncio.get_event_loop().run_until_complete(command.run(mock_cmdio))

        mock_send = mock_cmdio.message.channel.send
        mock_send.assert_called_once()
        self.assertEqual(mock_send.call_args[0], ('funfact', ))
        self.assertEqual(mock_send.call_args[1]['embed'].image.url, 'linkurl')


if __name__ == '__main__':
    unittest.main()
