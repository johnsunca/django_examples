# Generated by Django 5.0.2 on 2024-03-17 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelsapp', '0005_remove_entry_authors_remove_entry_blog_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='name',
            field=models.CharField(default=None, max_length=100, unique=True),
        ),
    ]
