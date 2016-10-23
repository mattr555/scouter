# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-22 21:41
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import restapi.models
import restapi.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('restapi', '0002_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='RobotProperties',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('props', restapi.models.JSONField(blank=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='robot_props', to=settings.AUTH_USER_MODEL)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='robot_props', to='restapi.Team')),
            ],
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='robot_fields',
            field=restapi.models.JSONField(blank=True, default=restapi.models.UserProfile.default_robot_fields, validators=[restapi.validators.robot_field_validator]),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='robotproperties',
            unique_together=set([('owner', 'team')]),
        ),
    ]