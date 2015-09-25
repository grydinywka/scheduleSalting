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
            (u'Лящ різаний', u'Лящ різаний'),
            (u'Лящ цілий', u'Лящ цілий'),
            (u'Сом філе', u'Сом філе'),
            (u'Товстолоб філе', u'Товстолоб філе'),
            (u'Судак', u'Судак'),
            (u'Густирь', u'Густирь'),
            (u'Сало, м’ясо', u'Сало, м’ясо'),
            (u'Карась різаний', u'Карась різаний'),
            (u'Карась цілий', u'Карась цілий'),
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
        return u'%s' % (self.id)

    def save(self, *args, **kwargs):
        deltaSalting = datetime.timedelta(days=int(self.required_salting))
        self.date_removing = self.date_salting + deltaSalting
        super(Salting, self).save(*args, **kwargs)

def validate_time(value):
    import time
    from django.core.exceptions import ValidationError

    try:
        time.strptime(value, "%H:%M")
    except:
        pass


class Reminder(models.Model):
    """Reminder Model"""

    class Meta(object):
        verbose_name = u'Нагадування'
        verbose_name_plural = u'Нагадування'

    time_reminding = models.TimeField(
        blank=False,
        verbose_name=u'Час відправлення листа на пошту',
        null=True
    )

    def __unicode__(self):
        return u'%s' % (self.time_reminding)

