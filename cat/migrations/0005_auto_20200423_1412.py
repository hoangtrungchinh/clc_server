# Generated by Django 3.0.4 on 2020-04-23 14:12

import cat.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cat', '0004_auto_20200423_1325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(upload_to=cat.models.File.get_upload_path),
        ),
    ]
