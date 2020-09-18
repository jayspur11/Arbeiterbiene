import json

from web import web_worker


class GeocodeWorker(web_worker.WebWorker):
    """Class to translate a zip code into city name + lat/long coordinates.
    
    Done using a query on OpenDataSoft.com.
    """
    def fetch(self, zip_code):
        """Retrieve city information.

        Args:
            zip_code (string): Zip code to be translated.

        Returns:
            dict{string:string}: City information, including `latitude`,
                `longitude`, and `city`.
        """
        url = ("https://public.opendatasoft.com/api/records/1.0/search?"
               "dataset=us-zip-code-latitude-and-longitude&q=zip={zip}".format(
                   zip=zip_code))
        return json.loads(self._make_request(url))
