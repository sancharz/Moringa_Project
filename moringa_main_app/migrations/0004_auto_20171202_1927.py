# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-03 00:27
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('moringa_main_app', '0003_auto_20171123_2308'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[(b'nairobi', b'NAIROBI, KENYA'), (b'mumbai', b'MUMBAI, INDIA')], max_length=20)),
                ('ip_addresses', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), size=None)),
            ],
        ),
        migrations.AlterField(
            model_name='localadmin',
            name='location',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='moringa_main_app.Location'),
        ),
    ]
