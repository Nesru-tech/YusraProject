# Generated by Django 4.2 on 2025-06-19 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tours", "0003_alter_vacationtour_country_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="contactmessage",
            name="phone_number",
            field=models.CharField(default="Unknown", max_length=20),
        ),
    ]
