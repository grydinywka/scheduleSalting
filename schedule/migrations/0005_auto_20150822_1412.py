# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0004_auto_20150822_1355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salting',
            name='status',
            field=models.CharField(default='\u0417\u0430\u0441\u043e\u043b\u043a\u0430 \u0442\u0440\u0438\u0432\u0430\u0454', max_length=50, verbose_name='\u0421\u0442\u0430\u0442\u0443\u0441', choices=[('\u0417\u0430\u0441\u043e\u043b\u043a\u0430 \u0432\u0438\u0442\u044f\u0433\u043d\u0443\u0442\u0430', '\u0417\u0430\u0441\u043e\u043b\u043a\u0430 \u0432\u0438\u0442\u044f\u0433\u043d\u0443\u0442\u0430'), ('\u0417\u0430\u0441\u043e\u043b\u043a\u0430 \u0442\u0440\u0438\u0432\u0430\u0454', '\u0417\u0430\u0441\u043e\u043b\u043a\u0430 \u0442\u0440\u0438\u0432\u0430\u0454')]),
        ),
    ]
