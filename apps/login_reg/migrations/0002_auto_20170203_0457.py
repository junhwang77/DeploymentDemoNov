# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-03 04:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login_reg', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='users',
            old_name='first_name',
            new_name='alias',
        ),
        migrations.RenameField(
            model_name='users',
            old_name='last_name',
            new_name='name',
        ),
    ]