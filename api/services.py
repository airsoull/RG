# standar libraries
import re
import requests
import logging

from base.parsers import HTMLParser

logger = logging.getLogger(__name__)

BASE_URL = 'https://coinmarketcap.com/'


def get_coinmarketcap_data(name: str) -> list:
    parser = HTMLParser()

    for i in range(1, 1000):
        content = get_coinmarketcap_content(i)

        # search currency name on coinmarketcap
        if not re.search(name, content):
            continue

        parser.feed(content)
        for data in parser.data:
            if name == data[1]:
                return data


def get_coinmarketcap_content(endpoint) -> str:
    return _get_content(f'{endpoint}/')


def _get_content(endpoint) -> str:
    try:
        response = requests.get(f'{BASE_URL}{endpoint}')
        response.raise_for_status()
        return response.text
    except requests.exceptions.ConnectionError as e:
        logger.error(e)
        raise e
    except requests.exceptions.HTTPError as e:
        logger.error(e)
        raise e
