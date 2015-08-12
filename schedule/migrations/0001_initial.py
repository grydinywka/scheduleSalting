# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Salting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_salting', models.DateField(null=True, verbose_name='\u0414\u0430\u0442\u0430 \u043f\u043e\u0441\u043e\u043b\u0443')),
                ('name_fish', models.CharField(max_length=256, verbose_name='\u041d\u0430\u0437\u0432\u0430 \u0440\u0438\u0431\u0438(\u0440\u0438\u0431)')),
                ('required_salting', models.CharField(max_length=2, verbose_name='\u0427\u0430\u0441 \u043d\u0430 \u0441\u043e\u043b\u0456\u043d\u043d\u044f(\u0434\u043d\u0456\u0432)')),
                ('tank_salting', models.CharField(max_length=256, verbose_name='\u0404\u043c\u043d\u0456\u0441\u0442\u044c \u0456 \u043c\u0456\u0441\u0446\u0435 \u043f\u043e\u0441.')),
                ('notes', models.TextField(verbose_name='\u0414\u043e\u0434\u0430\u0442\u043a\u043e\u0432\u0456 \u041d\u043e\u0442\u0430\u0442\u043a\u0438', blank=True)),
            ],
            options={
                'verbose_name': '\u0417\u0430\u0441\u043e\u043b\u043a\u0430',
                'verbose_name_plural': '\u0417\u0430\u0441\u043e\u043b\u043a\u0438',
            },
        ),
    ]
