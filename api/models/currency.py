# django
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

# base
from base.models import BaseModel

# managers
from api.managers import CurrencyQueryset
from api.managers import CurrencyManager


class Currency(BaseModel):
    name = models.CharField(
        _('name'),
        max_length=255,
        unique=True,
    )

    objects = CurrencyQueryset.as_manager()
    create = CurrencyManager()

    class Meta:
        verbose_name = _('currency')
        verbose_name_plural = _('currencies')

    def __str__(self):
        return self.name

    @property
    def frequency(self) -> int:
        return self.scrapper.frequency

    @property
    def value(self) -> float:
        return self.prices.last().value

    @property
    def value_updated_at(self):
        return self.prices.last().updated_at

    @classmethod
    def get_currencies_serializer(cls) -> dict:
        data = []
        for currency in cls.objects.related_objects():
            data.append(
                currency.get_currency_list_serializer()
            )
        return {'scrapers': data}

    @classmethod
    def create_currency_from_coinmarketcap(cls, data):
        valid_keys = sorted((
            'currency',
            'frequency',
        ))

        if not sorted(list(data.keys())) == valid_keys:
            raise ValidationError('invalid keys')

        # return currency if exists
        if cls.objects.filter(name=data['currency']).exists():
            return (
                cls.objects.get(name=data['currency'])
                .get_currency_retrieve_serializer()
            )

        try:
            currency = cls.create.create_currency_from_coinmarket(data)
        except Exception as e:
            raise e

        return currency.get_currency_retrieve_serializer()

    def get_currency_retrieve_serializer(self) -> dict:
        return {
            'id': self.pk,
            'created_at': self.created_at,
            'currency': self.name,
            'frequency': self.frequency,
        }

    def get_currency_list_serializer(self) -> dict:
        return {
            'value': self.value,
            'value_updated_at': self.value_updated_at,
            **self.get_currency_retrieve_serializer(),
        }
