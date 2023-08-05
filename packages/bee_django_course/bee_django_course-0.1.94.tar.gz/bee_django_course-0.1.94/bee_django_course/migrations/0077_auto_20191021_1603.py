# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2019-10-21 08:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bee_django_course', '0076_section_has_to_finish_course_video'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserCourseSectionVideo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('finish_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('user_course_section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bee_django_course.UserCourseSection')),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bee_django_course.Video')),
            ],
        ),
        migrations.AlterField(
            model_name='section',
            name='has_to_finish_course_video',
            field=models.BooleanField(default=False, verbose_name='\u662f\u5426\u9700\u8981\u770b\u5b8c\u8bfe\u4ef6\u6240\u6709\u89c6\u9891(\u53ea\u5bf9\u4e03\u725b\u4e91\u89c6\u9891\u6709\u6548)'),
        ),
    ]
