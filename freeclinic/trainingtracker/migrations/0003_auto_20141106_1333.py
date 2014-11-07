# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trainingtracker', '0002_auto_20141106_1314'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='name',
            field=models.CharField(default='Volunteer Group 1', unique=True, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='section',
            name='courses',
            field=models.ManyToManyField(to='trainingtracker.Course', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='section',
            name='jobs',
            field=models.ManyToManyField(to='trainingtracker.Job', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='section',
            name='skills',
            field=models.ManyToManyField(to='trainingtracker.Skill', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='section',
            name='timeslots',
            field=models.ManyToManyField(to='trainingtracker.Timeslot', null=True),
            preserve_default=True,
        ),
    ]
