# Generated by Django 2.2.5 on 2019-09-03 01:04

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0005_auto_20190819_1823'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='quantity_available',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(999)]),
        ),
        migrations.AlterField(
            model_name='product',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='market.User'),
        ),
    ]