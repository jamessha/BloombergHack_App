# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickerwatch', '0005_remove_userprofile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='carrier',
            field=models.CharField(default=b'att', max_length=15),
            preserve_default=True,
        ),
    ]
