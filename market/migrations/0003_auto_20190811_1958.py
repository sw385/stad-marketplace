# Generated by Django 2.2.4 on 2019-08-11 23:58

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0002_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_ordered', models.DateTimeField(auto_now_add=True)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0, help_text='Enter the subtotal for this order.', max_digits=6)),
                ('tax', models.DecimalField(decimal_places=2, default=0, help_text='Enter the tax for this order.', max_digits=6)),
                ('address', models.CharField(default='', max_length=255)),
                ('state', models.CharField(default='', max_length=30)),
                ('city', models.CharField(default='', max_length=30)),
                ('zip_code', models.CharField(default='', max_length=10)),
                ('payment_method', models.CharField(default='', max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID', primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=25)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('phone', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=30)),
                ('city', models.CharField(max_length=30)),
                ('zip_code', models.CharField(max_length=10)),
                ('payment_method', models.CharField(default='None', max_length=15)),
                ('order_seller', models.CharField(default='None', max_length=100)),
                ('order_buyer', models.CharField(default='None', max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['first_name', 'last_name'],
            },
        ),
        migrations.AddField(
            model_name='product',
            name='pictures',
            field=models.ManyToManyField(help_text='Select some pictures for this product.', to='market.Image'),
        ),
        migrations.CreateModel(
            name='OrderedProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)])),
                ('price', models.DecimalField(decimal_places=2, help_text='Enter the price of this product.', max_digits=6)),
                ('containing_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='market.Order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='market.Product')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='buyer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='market.User'),
        ),
        migrations.AddField(
            model_name='image',
            name='uploaded_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='market.User'),
        ),
        migrations.AddField(
            model_name='product',
            name='seller',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='market.User'),
        ),
    ]