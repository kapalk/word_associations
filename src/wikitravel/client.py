import os
import json

import logging
import logging.config

import requests

class WikitravelClient:

    def __init__(self):

        self.base_url = 'https://wikitravel.org/wiki/en/api.php'
        self.config_file = 'logging.ini'
        self.logger = self._get_logger()
        self.logger.info('Crawler created')

    def get_countries(self, countries):
        for country in countries:
            self.get_country(country)

    def get_country(self, country):

        params = {
            'action': 'parse',
            'page': country,
            'format': 'json'
        }

        response = self._get(self.base_url, params)
        
        if response.status_code != 200:
            return

        json_obj = response.json()

        if 'error' in json_obj.keys():
            error_code = json_obj['error']['code']
            self.logger.warning(
                "Error fetching {country}: {code}".format(country=country, code=error_code)
            )
            return
        
        with open(os.path.join('data', country + '.json'), 'w') as fp:
            json.dump(json_obj, fp, indent=4) 


    def _get_logging_level(self, status_code):

        return logging.INFO if status_code == 200 else logging.WARNING 
    
    def _get_logger(self):
        """
        Read logging config file and return a configured logger

        Configured logger contains following handlers:
            FileHandler: level=DEBUG
            StreamHandler: level=ERROR

        Returns:
            logging.logger
        """
        fname = os.path.join(os.path.dirname(__file__), self.config_file)
        logging.config.fileConfig(fname)
        return logging.getLogger(__name__)


    def _get(self, url, params=None):
        """
        Wrap requests.get with additional logging

        Params:
            url (string)
            params (dir):   Python directory object containing additional url params

        Returns:
            (requests.response) response
        """
        response = requests.get(url, params=params)
        logging_level = self._get_logging_level(response.status_code)
        self.logger.log(logging_level, '{status} - GET {url}'.format(status=response.status_code, url=response.url))
        return response

    def _parse_response(self, response):
        print(response.content)

def main():
    
    crawler = WikitravelClient()

    with open('countries.txt', 'r') as fp:
        countries = fp.readlines()
    countries = [country.strip() for country in countries]
    
    crawler.get_countries(countries[:50])
    
if __name__ == '__main__':
    main()
