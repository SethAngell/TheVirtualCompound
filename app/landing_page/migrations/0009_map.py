# Generated by Django 4.0.2 on 2022-06-01 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("landing_page", "0008_alter_favoritething_path_attribute"),
    ]

    operations = [
        migrations.CreateModel(
            name="Map",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("location_name", models.CharField(max_length=150)),
            ],
        ),
    ]