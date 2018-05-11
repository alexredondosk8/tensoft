# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-11 08:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('apellidos', models.CharField(max_length=100)),
                ('correo', models.CharField(max_length=254)),
                ('telefono', models.CharField(max_length=7)),
                ('celular', models.CharField(max_length=10)),
            ],
        ),
    ]
