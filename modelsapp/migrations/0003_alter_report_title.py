# Generated by Django 5.0.2 on 2024-03-17 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelsapp', '0002_report_title_alter_report_report_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='title',
            field=models.CharField(max_length=128),
        ),
    ]