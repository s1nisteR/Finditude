# Generated by Django 4.1.7 on 2023-05-22 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0004_missingpersonlocations"),
    ]

    operations = [
        migrations.AddField(
            model_name="missingpersonlocations",
            name="lattitude",
            field=models.CharField(default=0, max_length=2056),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="missingpersonlocations",
            name="longitude",
            field=models.CharField(default="0", max_length=2056),
            preserve_default=False,
        ),
    ]
