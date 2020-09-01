# django
from django.db import models
from django.utils.translation import ugettext_lazy as _

# base
from base.models import BaseModel


class Currency(BaseModel):
    external_id = models.CharField(
        _('external id'),
        max_length=255,
    )
    name = models.CharField(
        _('name'),
        max_length=255,
    )

    class Meta:
        verbose_name = _('currency')
        verbose_name_plural = _('currencies')

    def __str__(self):
        return self.name
