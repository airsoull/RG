# django
from django.db import models
from django.utils.translation import ugettext_lazy as _

# base
from base.models import BaseModel


class Scraper(BaseModel):
    currency = models.OneToOneField(
        'api.Currency',
        verbose_name=_('currency'),
        related_name='scrapper',
        on_delete=models.CASCADE,
    )
    frequency = models.PositiveIntegerField(
        _('frequency'),
    )

    class Meta:
        verbose_name = _('Scraper')
        verbose_name_plural = _('Scrapers')

    def update_frequency(self, new_frequency):
        self.frequency = new_frequency
        self.save()
