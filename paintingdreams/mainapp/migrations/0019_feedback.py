# Generated by Django 2.2.17 on 2021-03-14 09:51

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import mainapp.models.web_images


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0018_uk_only_products'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback', models.TextField()),
                ('author_name', models.CharField(blank=True, max_length=100)),
                ('author_email', models.EmailField(blank=True, max_length=254)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name_plural': 'Feedback items',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='FeedbackWebimage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('webimage', models.ImageField(upload_to=mainapp.models.web_images.get_webimage_path)),
                ('name', models.CharField(blank=True, max_length=100)),
                ('sizes', models.CharField(blank=True, max_length=255)),
                ('order', models.PositiveSmallIntegerField(blank=True, default=0)),
                ('feedback', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='webimages', to='mainapp.Feedback')),
            ],
            options={
                'ordering': ['order'],
                'abstract': False,
            },
        ),
    ]
