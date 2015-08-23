# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0003_salting_weight'),
    ]

    operations = [
        migrations.AddField(
            model_name='salting',
            name='status',
            field=models.BooleanField(default=False, verbose_name='\u0421\u0442\u0430\u0442\u0443\u0441'),
        ),
        migrations.AlterField(
            model_name='salting',
            name='name_fish',
            field=models.CharField(max_length=256, verbose_name='\u041d\u0430\u0437\u0432\u0430 \u0440\u0438\u0431\u0438(\u0440\u0438\u0431)', choices=[(b'Taran', b'Taran'), (b'Lyasch', b'Lyasch')]),
        ),
    ]
