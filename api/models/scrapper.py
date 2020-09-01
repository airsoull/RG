# django
from django.db import models
from django.utils.translation import ugettext_lazy as _

# base
from base.models import BaseModel


class Scraper(BaseModel):
    currency = models.ForeignKey(
        'api.Currency',
        verbose_name=_('currency'),
        related_name='scrappers',
        on_delete=models.CASCADE,
    )
    frequency = models.PositiveIntegerField(
        _('frequency'),
        default=60,
    )

    class Meta:
        verbose_name = _('Scraper')
        verbose_name_plural = _('Scrapers')
