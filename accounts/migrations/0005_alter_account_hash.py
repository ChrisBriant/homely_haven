# Generated by Django 4.1.3 on 2023-02-08 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_account_hash'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='hash',
            field=models.CharField(default='0x4b9a25a3bc0c947399e92113826ef316', max_length=128),
        ),
    ]