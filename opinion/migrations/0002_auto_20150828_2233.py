# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('opinion', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student_info',
            old_name='studnet_name',
            new_name='student_name',
        ),
    ]
