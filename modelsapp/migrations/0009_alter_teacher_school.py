# Generated by Django 5.0.2 on 2024-03-19 05:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelsapp', '0008_location_school_teacher_course'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='school',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='modelsapp.school'),
        ),
    ]
