# django
from django.db import models
from django.utils.translation import ugettext_lazy as _


class BaseModel(models.Model):
    """ An abstract class that every model should inherit from """
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('created at'),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        null=True,
        verbose_name=_('updated at'),
    )

    class Meta:
        abstract = True
