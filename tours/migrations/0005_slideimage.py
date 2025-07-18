# Generated by Django 4.2 on 2025-06-21 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tours", "0004_contactmessage_phone_number"),
    ]

    operations = [
        migrations.CreateModel(
            name="SlideImage",
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
                ("title", models.CharField(max_length=100)),
                ("image", models.ImageField(upload_to="slides/")),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
