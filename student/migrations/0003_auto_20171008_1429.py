# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import student.models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0002_auto_20170410_0005'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentdb',
            name='resume',
            field=models.FileField(blank=True, upload_to=student.models.content_file_name),
        ),
        migrations.AlterField(
            model_name='appliedjob',
            name='got_offer',
            field=models.CharField(default='No', max_length=250),
        ),
    ]
