# Generated by Django 4.1.3 on 2023-02-06 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='hash',
            field=models.CharField(default='0xa5ec36fb159b67ac467da3f6eba19460', max_length=128),
        ),
    ]