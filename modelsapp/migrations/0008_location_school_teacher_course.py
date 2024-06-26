# Generated by Django 5.0.2 on 2024-03-19 04:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelsapp', '0007_alter_employee_employee_id_alter_onecard_number_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('type', models.CharField(choices=[('preliminary', 'Preliminary'), ('middle', 'Middle'), ('high', 'High'), ('others', 'Others')], max_length=20)),
                ('location', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='modelsapp.location')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modelsapp.school')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('credit', models.IntegerField()),
                ('teachers', models.ManyToManyField(related_name='courses', to='modelsapp.teacher')),
            ],
        ),
    ]
