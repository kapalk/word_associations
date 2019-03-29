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

        self.countries = self._read_countries()
        self.data_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'data'))

        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            self.logger.info('Created directory {dir}'.format(dir=self.data_dir))
        
        self.logger.info('Using {dir} as data directory'.format(dir=self.data_dir))

    def get_countries(self, countries):
        for country in countries:
            self.get_country(country)

    def get_country(self, country):

        params = {
            'action': 'parse',
            'page': country,
            'format': 'json',
            'prop': 'wikitext'
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
        
        self._save_json(json_obj, country)

    def _save_json(self, json_obj, country):
        path = os.path.join(self.data_dir, country + '.json')
        with open(path, 'w') as fp:
            json.dump(json_obj, fp, indent=4)
    def _read_countries(self):

        path = os.path.join(os.path.dirname(__file__), 'countries.txt')
        with open(path, 'r') as fp:
            countries = fp.readlines()

        return [country.strip().replace('{', '').replace('}', '') for country in countries]

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
    crawler.get_countries(crawler.countries[:10])
    
if __name__ == '__main__':
    main()
