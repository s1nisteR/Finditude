# Generated by Django 4.1.7 on 2023-05-21 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="myFindings",
            field=models.JSONField(default=list),
        ),
        migrations.AddField(
            model_name="user",
            name="myReports",
            field=models.JSONField(default=list),
        ),
    ]
