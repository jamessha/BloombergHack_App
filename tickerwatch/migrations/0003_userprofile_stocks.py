# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickerwatch', '0002_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='stocks',
            field=models.ManyToManyField(to='tickerwatch.Stock'),
            preserve_default=True,
        ),
    ]
