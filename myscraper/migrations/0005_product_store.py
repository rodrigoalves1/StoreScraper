# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-20 15:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myscraper', '0004_product_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='store',
            field=models.CharField(choices=[('ka', 'Kanui'), ('ns', 'netshoes')], default='ka', max_length=2),
        ),
    ]