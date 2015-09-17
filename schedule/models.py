# -*- coding: utf-8 -*-

from django.db import models
import datetime

def dec(mCls):
    setattr(mCls, "date_removing", 15)
    return mCls

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
        verbose_name=u'Назва риби(риб)',
        choices=(
            (u'Тарань', u'Тарань'),
            (u'Лящ цілий', u'Лящ цілий'),
            (u'Лящ різаний', u'Лящ різаний'),
            (u'Товстолоб філе', u'Товстолоб філе'),
            (u'Сом філе', u'Сом філе'),
            (u'Густир', u'Густир'),
            (u'Судак', u'Судак'),
            (u'Судак різаний', u'Судак різаний'),
            (u'Карась цілий', u'Карась цілий'),
            (u'Карась різаний', u'Карась різаний'),
            (u'Короп цілий', u'Короп цілий'),
            (u'Короп різаний', u'Короп різаний'),
        )
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

    date_removing = models.DateField(
        blank=True,
        verbose_name=u'Дата виємки',
        null=True,
        editable=False
    )

    weight = models.CharField(
        max_length=256,
        blank=True,
        verbose_name=u'Кількість риби'
    )

    status = models.BooleanField(
        blank=False,
        verbose_name=u'Статус',
        default=True,
        choices=(
            (False, u'Засолка витягнута'),
            (True, u'Засолка триває'),
        )
    )

    def __unicode__(self):
        return u'%s, %s' % (self.date_salting, self.name_fish)

    def save(self, *args, **kwargs):
        deltaSalting = datetime.timedelta(days=int(self.required_salting))
        self.date_removing = self.date_salting + deltaSalting
        super(Salting, self).save(*args, **kwargs)