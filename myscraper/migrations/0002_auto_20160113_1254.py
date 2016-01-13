# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myscraper', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='size',
            field=models.CharField(max_length=300, blank=True),
        ),
    ]
