# Generated by Django 5.0.2 on 2024-03-28 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelsapp', '0011_person'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='children',
            field=models.ManyToManyField(blank=True, to='modelsapp.person'),
        ),
    ]
