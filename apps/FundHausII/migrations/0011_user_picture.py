# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-02-25 17:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FundHausII', '0010_remove_project_percentage'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='picture',
            field=models.ImageField(blank=True, upload_to='user_image'),
        ),
    ]
