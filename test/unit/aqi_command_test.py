import asyncio
import commands
import json
import urllib
import unittest

from test.shared import async_mock


class AqiCommandTest(unittest.TestCase):
    @unittest.mock.patch('urllib.request.urlopen')
    def test_basic_command(self, mock_urlopen):
        with mock_urlopen() as mock_response:
            mock_response.read.return_value = b"""
                [
                    {
                        "ParameterName": "paramName",
                        "AQI": "aqiValue",
                        "Category": {
                            "Name": "categoryName"
                        }
                    }
                ]
            """
        mock_urlopen.reset_mock()
        mock_cmdio = async_mock.AsyncMock()
        mock_cmdio.message.channel.typing = unittest.mock.MagicMock()
        mock_cmdio.message.content = '12345'
        command = commands.AqiCommand('fakeAPIkey')

        asyncio.get_event_loop().run_until_complete(command.run(mock_cmdio))

        mock_urlopen.assert_called_once()
        requested_url = mock_urlopen.call_args[0][0].full_url
        self.assertIn('zipCode=12345', requested_url)
        self.assertIn('api_key=fakeAPIkey', requested_url)

        mock_send = mock_cmdio.message.channel.send
        mock_send.assert_called_once()
        sent_message = mock_send.call_args[0][0]
        self.assertIn('paramName', sent_message)
        self.assertIn('aqiValue', sent_message)
        self.assertIn('categoryName', sent_message)


if __name__ == '__main__':
    unittest.main()
