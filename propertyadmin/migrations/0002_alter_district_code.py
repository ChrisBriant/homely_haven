# Generated by Django 4.1.3 on 2023-02-04 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('propertyadmin', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='district',
            name='code',
            field=models.CharField(max_length=5, unique=True),
        ),
    ]
