# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import schedule.models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0004_auto_20150824_0819'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reminder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_reminding', models.TimeField(null=True, verbose_name='\u0427\u0430\u0441 \u0432\u0456\u0434\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u043d\u044f \u043b\u0438\u0441\u0442\u0430 \u043d\u0430 \u043f\u043e\u0448\u0442\u0443', validators=[schedule.models.validate_time])),
            ],
            options={
                'verbose_name': '\u041d\u0430\u0433\u0430\u0434\u0443\u0432\u0430\u043d\u043d\u044f',
                'verbose_name_plural': '\u041d\u0430\u0433\u0430\u0434\u0443\u0432\u0430\u043d\u043d\u044f',
            },
        ),
    ]
