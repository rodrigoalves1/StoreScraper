# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myscraper', '0003_auto_20160113_1257'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='status',
            field=models.CharField(max_length=1, choices=[('e', 'Enabled'), ('d', 'Disabled')], default='e'),
        ),
    ]
