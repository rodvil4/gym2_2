# Generated by Django 5.1.5 on 2025-07-24 00:08

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0010_member_pagos_real'),
    ]

    operations = [
        migrations.AddField(
            model_name='pago',
            name='fec_reg',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True, verbose_name='Fecha de Registro'),
        ),
    ]
