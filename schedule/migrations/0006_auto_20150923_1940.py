# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0005_reminder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reminder',
            name='time_reminding',
            field=models.TimeField(null=True, verbose_name='\u0427\u0430\u0441 \u0432\u0456\u0434\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u043d\u044f \u043b\u0438\u0441\u0442\u0430 \u043d\u0430 \u043f\u043e\u0448\u0442\u0443'),
        ),
    ]
