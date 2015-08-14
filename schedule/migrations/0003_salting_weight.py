# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0002_salting_date_removing'),
    ]

    operations = [
        migrations.AddField(
            model_name='salting',
            name='weight',
            field=models.CharField(max_length=256, verbose_name='\u041a\u0456\u043b\u044c\u043a\u0456\u0441\u0442\u044c \u0440\u0438\u0431\u0438', blank=True),
        ),
    ]
