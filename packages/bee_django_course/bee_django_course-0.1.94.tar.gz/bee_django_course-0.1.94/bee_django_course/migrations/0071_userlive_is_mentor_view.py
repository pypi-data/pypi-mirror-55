# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2019-09-06 08:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bee_django_course', '0070_userlive_is_star'),
    ]

    operations = [
        migrations.AddField(
            model_name='userlive',
            name='is_mentor_view',
            field=models.BooleanField(default=False),
        ),
    ]
