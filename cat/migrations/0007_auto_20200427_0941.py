# Generated by Django 3.0.4 on 2020-04-27 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cat', '0006_auto_20200425_1439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sentence',
            name='is_confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='sentence',
            name='score',
            field=models.FloatField(default=0),
        ),
    ]
