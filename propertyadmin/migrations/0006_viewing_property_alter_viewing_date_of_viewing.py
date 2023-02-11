# Generated by Django 4.1.3 on 2023-02-08 05:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('propertyadmin', '0005_viewing_date_of_viewing_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='viewing',
            name='property',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='propertyadmin.property'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='viewing',
            name='date_of_viewing',
            field=models.DateField(default=None),
        ),
    ]
