from urllib import request
from web import web_hive

class WebWorker:
    """Class to fetch information from the web."""
    cache = web_hive.WebHive()

    def __init__(self):
        self.ttl = None

    def fetch(self, url):
        return self._make_request(url)
    
    def _make_request(self, url):
        """Retrieve data from the given URL.

        Args:
            url (string): The URL to retrieve data from.

        Returns:
            string: The decoded response.
        """
        cached = self.cache.get(url)
        if cached:
            return cached
        
        web_request = request.Request(url, headers={
            "User-Agent": "arbeiterbiene"
        })
        with request.urlopen(web_request) as response:
            result = response.read().decode()
        self.cache.store(url, result, self.ttl)
        return result
