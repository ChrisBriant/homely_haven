# Generated by Django 4.1.3 on 2023-02-09 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_account_hash'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='hash',
            field=models.CharField(default='0x7b2e77bfd89504bfe09ca7a12e17cffd', max_length=128),
        ),
    ]
