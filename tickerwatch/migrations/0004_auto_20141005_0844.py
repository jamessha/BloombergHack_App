# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tickerwatch', '0003_userprofile_stocks'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='stocks',
        ),
        migrations.AddField(
            model_name='stock',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
