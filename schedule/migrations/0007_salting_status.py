# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0006_auto_20150823_0704'),
    ]

    operations = [
        migrations.AddField(
            model_name='salting',
            name='status',
            field=models.BooleanField(default='\u0417\u0430\u0441\u043e\u043b\u043a\u0430 \u0442\u0440\u0438\u0432\u0430\u0454', verbose_name='\u0421\u0442\u0430\u0442\u0443\u0441', choices=[(False, '\u0417\u0430\u0441\u043e\u043b\u043a\u0430 \u0432\u0438\u0442\u044f\u0433\u043d\u0443\u0442\u0430'), (True, '\u0417\u0430\u0441\u043e\u043b\u043a\u0430 \u0442\u0440\u0438\u0432\u0430\u0454')]),
        ),
    ]
