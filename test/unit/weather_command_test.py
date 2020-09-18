import asyncio
import commands
import json
import urllib
import unittest

from test.shared import async_mock
from unittest import mock


def urlopen_mocked(req):
    mock_response = mock.Mock()
    if "opendatasoft" in req.full_url:
        mock_response.read.return_value = b"""
            {
                "records": [{
                    "fields": {
                        "latitude": "lat",
                        "longitude": "long",
                        "city": "Townsville"
                    }
                }]
            }"""
    elif "openweathermap" in req.full_url:
        mock_response.read.return_value = b"""
        {
            "current": {
                "temp": "451",
                "weather": [{
                    "description": "fire"
                }],
                "feels_like": "42"
            },
            "daily": [{
                "temp": {
                    "min": "0",
                    "max": "1000"
                },
                "weather": [{
                    "description": "numb"
                }]
            }]
        }"""
    mock_context_manager = mock.MagicMock()
    mock_context_manager.__enter__.return_value = mock_response
    return mock_context_manager

class WeatherCommandTest(unittest.TestCase):
    @unittest.mock.patch('urllib.request.urlopen', side_effect=urlopen_mocked)
    def test_basic_command(self, mock_urlopen):
        mock_cmdio = async_mock.AsyncMock()
        mock_cmdio.message.content = "12345"
        command = commands.WeatherCommand("apikey")
        asyncio.get_event_loop().run_until_complete(command.run(mock_cmdio))

        mock_send = mock_cmdio.message.channel.send
        mock_send.assert_called_once()

if __name__ == "__main__":
    unittest.main()
