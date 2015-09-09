# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='variant',
            name='created_by',
        ),
    ]
