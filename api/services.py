# standar libraries
import re
import requests
import logging

logger = logging.getLogger(__name__)

BASE_URL = 'https://coinmarketcap.com/'


def get_coinmarketcap_data() -> list:
    coinmarket_data = re.findall(
        r'<tr class="cmc-table-row" [^>]*>(?:.|\n)*?</tr>',
        get_all_coins_from_coinmarketcap()
    )

    for i, data in enumerate(coinmarket_data):
        coinmarket_data[i] = re.findall(
            r'[^>[^<]+<',
            data
        )
    return coinmarket_data


def get_content(endpoint):
    try:
        response = requests.get(f'{BASE_URL}{endpoint}')
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        logger.error(e)
        raise e


def get_all_coins_from_coinmarketcap():
    return get_content('coins/views/all/')
