# Generated by Django 5.0.2 on 2024-03-17 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelsapp', '0006_alter_department_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='employee_id',
            field=models.IntegerField(default=None, unique=True),
        ),
        migrations.AlterField(
            model_name='onecard',
            name='number',
            field=models.IntegerField(default=None, unique=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(default=None, max_length=128, unique=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='title',
            field=models.CharField(default=None, max_length=128, unique=True),
        ),
    ]
