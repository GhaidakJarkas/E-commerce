# Generated by Django 4.1.1 on 2022-09-29 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="digital",
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
