# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0005_auto_20150822_1412'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salting',
            name='status',
        ),
        migrations.AlterField(
            model_name='salting',
            name='date_removing',
            field=models.DateField(verbose_name='\u0414\u0430\u0442\u0430 \u0432\u0438\u0454\u043c\u043a\u0438', null=True, editable=False, blank=True),
        ),
    ]
