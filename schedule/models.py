# -*- coding: utf-8 -*-

from django.db import models

class Salting(models.Model):
    """Salting Model"""

    class Meta(object):
        verbose_name = u'Засолка'
        verbose_name_plural = u'Засолки'

    date_salting = models.DateField(
        blank=False,
        verbose_name=u'Дата посолу',
        null=True
    )

    name_fish = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u'Назва риби(риб)'
    )

    required_salting = models.CharField(
        max_length=2,
        blank=False,
        verbose_name=u'Час на соління(днів)'
    )

    tank_salting = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u'Ємність і місце пос.'
    )

    notes = models.TextField(
        blank=True,
        verbose_name=u'Додаткові Нотатки'
    )

    def __unicode__(self):
        return u'%s, %s' % (self.date_salting, self.name_fish)