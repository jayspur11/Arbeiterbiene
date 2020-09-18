class WebHive:
    """Class to cache information from the web."""
    class WebCell:
        """Individual cache entry in a WebHive."""
        def __init__(self, data, ttl):
            self.data = data
            # todo: convert to datetime
            self._expiry = ttl

        def expired(self):
            """Check whether the data has expired.

            Returns:
                bool: True if the data is expired, False otherwise.
            """
            if not self._expiry:
                return False
            # todo: check expiry against current time
            return True

    def __init__(self):
        self.cells = {}

    def get(self, key):
        """Retrieve data from the cache.

        Args:
            key (string): The key the value was stored with (probably a URL).

        Returns:
            The value that was stored.
        """        
        if key not in self.cells:
            return None
        cell = self.cells[key]
        if cell.expired():
            del self.cells[key]
            return None
        return cell.data

    def store(self, key, data, ttl):
        """Save data in the cache.

        Args:
            key (string): The key to store the value under (probably a URL).
            data (object): The data to be saved.
            ttl (int, optional): Time until data expires, in seconds.
                Pass None for no expiration. Defaults to None.
        """
        self.cells[key] = self.WebCell(data, ttl)
