# Generated by Django 4.1.7 on 2023-05-22 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0003_missingperson_contact"),
    ]

    operations = [
        migrations.CreateModel(
            name="MissingPersonLocations",
            fields=[
                ("uuid", models.BigAutoField(primary_key=True, serialize=False)),
            ],
        ),
    ]
