
# django
from django.test import TestCase
from django.urls import reverse

# models
from api.models import Currency
from api.models import Scraper
from api.models import Price


class ScraperAPITestCase(TestCase):

    def setUp(self):
        self.url = reverse('scrapers')
        self.currency_name = 'Bitcoin'

    def test_get(self):
        currency = Currency.objects.create(name=self.currency_name)
        Scraper.objects.create(currency=currency, frequency=60)
        Price.objects.create(currency=currency, value=2000)

        currency2 = Currency.objects.create(name='foo-bar')
        Scraper.objects.create(currency=currency2, frequency=60)
        Price.objects.create(currency=currency2, value=2000)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.json().keys()),
            ['scrapers'],
        )
        self.assertEqual(
            len(response.json()['scrapers']),
            Currency.objects.count(),
        )

        expected_data = [
            {
                'id': currency.id,
                'created_at': str(currency.created_at),
                'currency': currency.name,
                'frequency': currency.frequency,
                'value': currency.value,
                'value_updated_at': currency.value_updated_at,
            },
            {
                'id': currency2.id,
                'created_at': str(currency2.created_at),
                'currency': currency2.name,
                'frequency': currency2.frequency,
                'value': currency2.value,
                'value_updated_at': currency2.value_updated_at,

            }
        ]

        self.assertEqual(
            [sorted(d) for d in response.json()['scrapers']],
            [sorted(d) for d in expected_data],
        )

    def test_post(self):
        self.assertEqual(
            Currency.objects.count(),
            0
        )

        data = {
            'currency': 'Bitcoin',
            'frequency': 60,
        }
        response = self.client.post(
            self.url,
            data=data,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            Currency.objects.count(),
            1
        )

        currency = Currency.objects.get()
        expected_data = {
            'id': currency.id,
            'created_at': str(currency.created_at),
            'currency': currency.name,
            'frequency': currency.frequency,
        }
        self.assertEqual(
            sorted(response.json()),
            sorted(expected_data),
        )

    def test_put(self):
        currency = Currency.objects.create(name=self.currency_name)
        Scraper.objects.create(currency=currency, frequency=60)

        data = {
            'id': currency.pk,
            'frequency': 240,
        }
        response = self.client.put(
            self.url,
            data=data,
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            sorted(response.json().keys()),
            ['msg'],
        )

        currency.refresh_from_db()
        self.assertEqual(
            currency.frequency,
            data['frequency'],
        )

    def test_delete(self):
        currency = Currency.objects.create(name=self.currency_name)
        self.assertEqual(
            Currency.objects.count(),
            1
        )

        data = {
            'id': currency.pk,
        }
        response = self.client.delete(
            self.url,
            data=data,
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            sorted(response.json().keys()),
            ['msg'],
        )

        self.assertEqual(
            Currency.objects.count(),
            0
        )
