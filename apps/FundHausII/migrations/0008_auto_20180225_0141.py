# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-02-25 01:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FundHausII', '0007_auto_20180225_0113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='picture',
            field=models.FileField(blank=True, upload_to='project_image'),
        ),
    ]
