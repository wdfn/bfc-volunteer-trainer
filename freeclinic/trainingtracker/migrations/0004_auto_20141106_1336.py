# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trainingtracker', '0003_auto_20141106_1333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='courses',
            field=models.ManyToManyField(to='trainingtracker.Course', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='section',
            name='jobs',
            field=models.ManyToManyField(to='trainingtracker.Job', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='section',
            name='skills',
            field=models.ManyToManyField(to='trainingtracker.Skill', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='section',
            name='timeslots',
            field=models.ManyToManyField(to='trainingtracker.Timeslot', null=True, blank=True),
            preserve_default=True,
        ),
    ]
