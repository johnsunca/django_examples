# Generated by Django 5.0.2 on 2024-03-24 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bmsapp', '0003_alter_publisher_options_publisher_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publisher',
            name='address',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='publisher',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]