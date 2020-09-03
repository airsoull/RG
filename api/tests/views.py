
# django
from django.test import TestCase
from django.urls import reverse

# models
from api.models import Currency
from api.models import Scraper


class ScraperAPITestCase(TestCase):

    def setUp(self):
        self.url = reverse('scrapers')
        self.currency_name = 'Bitcoin'

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.json().keys()),
            ['scrapers'],
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
