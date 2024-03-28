# Generated by Django 5.0.2 on 2024-03-26 04:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=10)),
                ('campus', models.CharField(choices=[('brampton', 'Brampton'), ('mississauga', 'Mississauga'), ('oakville', 'Oakville')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('credit', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('student_id', models.CharField(max_length=20, unique=True)),
                ('date_of_birth', models.DateField()),
                ('address', models.TextField()),
                ('is_international', models.BooleanField(default=False)),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='studentmgmtsys.department')),
            ],
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark', models.FloatField()),
                ('enroll_date', models.DateField()),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studentmgmtsys.student')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studentmgmtsys.subject')),
            ],
        ),
        migrations.AddField(
            model_name='student',
            name='subjects',
            field=models.ManyToManyField(through='studentmgmtsys.Enrollment', to='studentmgmtsys.subject'),
        ),
    ]
