# django
from django.db import models
from django.utils.translation import ugettext_lazy as _

# base
from base.models import BaseModel

# utils
from api.utils import compare_keys
from api.utils import valid_if_is_float
from api.utils import get_obj_by_pk
from api.utils import default_json_message

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
        if hasattr(self, 'price_value'):
            return self.price_value[0].value
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
        valid_keys = (
            'currency',
            'frequency',
        )
        compare_keys(data, valid_keys)
        valid_if_is_float(data['frequency'])

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

    @classmethod
    def update_frequency(cls, data):
        valid_keys = (
            'id',
            'frequency',
        )
        compare_keys(data, valid_keys)
        valid_if_is_float(data['frequency'])

        currency = get_obj_by_pk(cls, data['id'], 'Currency doesn\'t exists.')
        currency.scrapper.update_frequency(data['frequency'])

        return default_json_message(
            f'Frequency of "{currency.name}" updated to {currency.frequency}'
        )

    @classmethod
    def delete_currency(cls, data):
        valid_keys = (
            'id',
        )
        compare_keys(data, valid_keys)

        currency = get_obj_by_pk(cls, data['id'], 'Currency doesn\'t exists.')
        currency.delete()

        return default_json_message(
            f'Currency "{currency.name}" was deleted.'
        )

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
