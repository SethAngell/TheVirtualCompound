# Generated by Django 4.0.7 on 2023-02-04 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_alter_blogpost_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topictags',
            name='tag_name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]