# Generated by Django 4.0.7 on 2023-07-02 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0016_alter_landingpage_bio_alter_landingpage_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='landingpage',
            name='headline',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
