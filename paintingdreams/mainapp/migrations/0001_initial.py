# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django_countries.fields
import mainapp.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ImageWebimage',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('webimage', models.ImageField(upload_to=mainapp.models.get_webimage_path)),
                ('name', models.CharField(max_length=100, blank=True)),
                ('order', models.PositiveSmallIntegerField(default=0, blank=True)),
                ('image', models.ForeignKey(to='mainapp.Image', related_name='webimages')),
            ],
            options={
                'ordering': ['order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('unique_id', models.CharField(max_length=50, default='b35b43b2-c830-463d-9ea1-94290749ed42', blank=True)),
                ('customer_id', models.IntegerField(null=True, blank=True)),
                ('customer_name', models.CharField(max_length=100)),
                ('customer_email', models.EmailField(max_length=254)),
                ('sub_total_price', models.DecimalField(max_digits=6, default=0, decimal_places=2)),
                ('postage_price', models.DecimalField(max_digits=6, default=0, decimal_places=2)),
                ('total_price', models.DecimalField(max_digits=6, default=0, decimal_places=2)),
                ('payment_processor', models.CharField(max_length=8, null=True, blank=True, choices=[('paypal', 'PayPal'), ('cardsave', 'CardSave')])),
                ('state', models.CharField(max_length=18, default='new', choices=[('new', 'New'), ('payment_started', 'Payment started'), ('payment_cancelled', 'Payment cancelled'), ('payment_processing', 'Payment processing'), ('payment_complete', 'Payment complete'), ('payment_failed', 'Payment failed'), ('shipped', 'Order shipped')])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrderLine',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('price', models.DecimalField(max_digits=6, default=0, decimal_places=2)),
                ('quantity', models.SmallIntegerField()),
                ('sub_total_price', models.DecimalField(max_digits=6, default=0, decimal_places=2)),
                ('order', models.ForeignKey(to='mainapp.Order')),
            ],
        ),
        migrations.CreateModel(
            name='PostagePrice',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('destination', models.CharField(max_length=6, choices=[('GB', 'United Kingdom'), ('EUROPE', 'Europe'), ('WORLD', 'Worldwide')])),
                ('min_weight', models.PositiveSmallIntegerField(default=0)),
                ('max_weight', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('price', models.DecimalField(max_digits=6, default=0, decimal_places=2)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('sold_out', models.BooleanField(default=False)),
                ('more_due', models.BooleanField(default=True)),
                ('due_text', models.CharField(max_length=255, blank=True)),
                ('extra_description', models.TextField(blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('image', models.ForeignKey(to='mainapp.Image', default=None, null=True, blank=True)),
            ],
            options={
                'ordering': ['product_type', '-image'],
            },
        ),
        migrations.CreateModel(
            name='ProductTag',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('title', models.CharField(max_length=100)),
                ('displayname', models.CharField(max_length=100, blank=True)),
                ('inherit_displayname', models.BooleanField(default=False)),
                ('description', models.TextField(blank=True)),
                ('inherit_description', models.BooleanField(default=False)),
                ('stand_alone', models.BooleanField(default=False)),
                ('inherit_stand_alone', models.BooleanField(default=True)),
                ('price', models.DecimalField(max_digits=6, default=0, blank=True, decimal_places=2)),
                ('inherit_price', models.BooleanField(default=True)),
                ('shipping_weight', models.IntegerField(default=0)),
                ('inherit_shipping_weight', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('parent', models.ForeignKey(to='mainapp.ProductType', default=None, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductWebimage',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('webimage', models.ImageField(upload_to=mainapp.models.get_webimage_path)),
                ('name', models.CharField(max_length=100, blank=True)),
                ('order', models.PositiveSmallIntegerField(default=0, blank=True)),
                ('product', models.ForeignKey(to='mainapp.Product', related_name='webimages')),
            ],
            options={
                'ordering': ['order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserAddress',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('address1', models.CharField(max_length=255)),
                ('address2', models.CharField(max_length=255, blank=True)),
                ('address3', models.CharField(max_length=255, blank=True)),
                ('address4', models.CharField(max_length=255, blank=True)),
                ('city', models.CharField(max_length=255, blank=True)),
                ('state', models.CharField(max_length=255, blank=True)),
                ('post_code', models.CharField(max_length=255, blank=True)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='product_type',
            field=models.ForeignKey(to='mainapp.ProductType'),
        ),
        migrations.AddField(
            model_name='product',
            name='tags',
            field=models.ManyToManyField(to='mainapp.ProductTag', default=None, blank=True),
        ),
        migrations.AddField(
            model_name='orderline',
            name='product',
            field=models.ForeignKey(to='mainapp.Product', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='order',
            name='customer_address',
            field=models.ForeignKey(to='mainapp.UserAddress'),
        ),
        migrations.AddField(
            model_name='image',
            name='products',
            field=models.ManyToManyField(to='mainapp.ProductType', through='mainapp.Product'),
        ),
        migrations.AddField(
            model_name='image',
            name='tags',
            field=models.ManyToManyField(to='mainapp.Tag', default=None, blank=True),
        ),
    ]
