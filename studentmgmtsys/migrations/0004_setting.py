# Generated by Django 5.0.2 on 2024-03-27 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentmgmtsys', '0003_alter_enrollment_enroll_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stage', models.IntegerField(blank=True, default=1, null=True)),
                ('reserve1', models.IntegerField(blank=True, default=1, null=True)),
                ('reserve2', models.IntegerField(blank=True, default=1, null=True)),
                ('reserve3', models.BooleanField(blank=True, default=False, null=True)),
                ('reserve4', models.BooleanField(blank=True, default=False, null=True)),
            ],
        ),
    ]
