# django
from django.db import models
from django.utils.translation import ugettext_lazy as _

# base
from base.models import BaseModel


class Price(BaseModel):
    currency = models.ForeignKey(
        'api.Currency',
        verbose_name=_('currency'),
        related_name='prices',
        on_delete=models.CASCADE
    )
    value = models.FloatField(
        _('value'),
    )

    class Meta:
        ordering = ('created_at',)
        verbose_name = _('price')
        verbose_name_plural = _('prices')
