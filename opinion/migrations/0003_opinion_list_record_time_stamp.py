# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('opinion', '0002_auto_20150828_2233'),
    ]

    operations = [
        migrations.AddField(
            model_name='opinion_list',
            name='record_time_stamp',
            field=models.CharField(default='0', max_length=20),
            preserve_default=False,
        ),
    ]
