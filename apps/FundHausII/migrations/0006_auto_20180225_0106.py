# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-02-25 01:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FundHausII', '0005_auto_20180215_0125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='picture',
            field=models.ImageField(blank=True, upload_to='media/project_image'),
        ),
    ]
