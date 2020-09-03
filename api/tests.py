# django
from django.test import TestCase
from django.core.validators import ValidationError

# requests
from requests.exceptions import HTTPError

# models
from api.models import Currency


class CurrencyTestCase(TestCase):

    def test_create_currency_from_coinmarketcap(self):
        self.assertEqual(
            Currency.objects.count(),
            0
        )

        data = {
            'currency': 'Bitcoin',
            'frequency': 20,
        }

        data = Currency.create_currency_from_coinmarketcap(data)
        self.assertEqual(
            Currency.objects.count(),
            1
        )

        currency = Currency.objects.get()

        self.assertEqual(currency.name, data['currency'])
        self.assertEqual(currency.frequency, data['frequency'])
        self.assertEqual(currency.prices.count(), 1)
        self.assertEqual(
            sorted(data.keys()),
            sorted(currency.get_currency_retrieve_serializer().keys())
        )

    def test_create_currency_from_coinmarketcap_not_repeat_currency(self):
        data = {
            'currency': 'Bitcoin',
            'frequency': 20,
        }

        Currency.create_currency_from_coinmarketcap(data)
        currency = Currency.objects.first()

        Currency.create_currency_from_coinmarketcap(data)
        currency2 = Currency.objects.last()

        self.assertEqual(
            Currency.objects.count(),
            1
        )
        self.assertEqual(currency, currency2)
        self.assertEqual(currency.value, currency2.value)

    def test_create_currency_from_coinmarketcap_invalid_data(self):
        data = {
            'foo': 'Bitcoin',
            'bar': 20,
        }

        with self.assertRaises(ValidationError):
            Currency.create_currency_from_coinmarketcap(data)

        self.assertEqual(
            Currency.objects.count(),
            0
        )

    def test_create_currency_from_coinmarketcap_invalid_currency(self):
        data = {
            'currency': 'invalid-currency-foo',
            'frequency': 20,
        }

        with self.assertRaises(HTTPError):
            Currency.create_currency_from_coinmarketcap(data)

        self.assertEqual(
            Currency.objects.count(),
            0
        )
