# Generated by Django 5.0.2 on 2024-03-24 19:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bmsapp', '0002_alter_publisher_options_remove_publisher_address_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='publisher',
            options={'ordering': ['-name']},
        ),
        migrations.AddField(
            model_name='publisher',
            name='address',
            field=models.CharField(default='123', max_length=50),
        ),
        migrations.AddField(
            model_name='publisher',
            name='city',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='publisher',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bmsapp.country'),
        ),
        migrations.AddField(
            model_name='publisher',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AddField(
            model_name='publisher',
            name='name',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='publisher',
            name='state_province',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='publisher',
            name='website',
            field=models.URLField(blank=True, null=True),
        ),
    ]
