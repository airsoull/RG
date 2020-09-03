# django
from django.db import models
from django.apps import apps

# requests
from requests.exceptions import ConnectionError
from requests.exceptions import HTTPError

# services
from api import services

# utils
from base.utils import str_from_coinmarket_to_float


class CurrencyQueryset(models.QuerySet):

    def related_objects(self):
        return (
            self.select_related('scrapper')
            .prefetch_related('prices')
        )


class CurrencyManager(models.Manager):

    def create_currency_from_coinmarket(self, data):
        try:
            coinmarketcap_data = (
                services.get_coinmarketcap_data(data['currency'])
            )
        except ConnectionError:
            raise ConnectionError('Error connecting with the server.')
        except HTTPError:
            raise HTTPError(
                f'Currency {data["currency"]} doesn\'t '
                'exists on coinmarketcap.com.'
            )
        except KeyError:
            raise KeyError('Invalid Currency.')

        Scraper = apps.get_model('api', 'Scraper')

        name = coinmarketcap_data[1]
        value = str_from_coinmarket_to_float(coinmarketcap_data[3])

        # create currency
        currency, created = self.model.objects.get_or_create(
            name=name,
        )

        if created:
            # create scrapper with frequency
            Scraper.objects.get_or_create(
                currency_id=currency.pk,
                defaults={
                    'frequency': data['frequency'],
                }
            )
            # create currency price with value
            currency.prices.create(value=value)

        return currency
