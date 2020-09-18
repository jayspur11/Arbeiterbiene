from urllib import request
from web import web_hive

class WebWorker:
    """Class to fetch information from the web."""
    cache = web_hive.WebHive()

    def __init__(self):
        self.ttl = None

    def fetch(self, url):
        """Perform the data retrieval.

        At this level, this is just a wrapper for `_make_request`; subclasses
        should override this method to provide more specialized interfaces (i.e.
        take in only the dynamic pieces of the request, and return a
        fully-processed object).

        Args:
            url (string): The URL to fetch from.

        Returns:
            string: The decoded response.
        """
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
