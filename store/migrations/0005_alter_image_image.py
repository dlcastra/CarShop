# Generated by Django 4.2.7 on 2023-12-14 08:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0004_image_alter_cartype_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="image",
            name="image",
            field=models.FileField(blank=True, upload_to="car-images"),
        ),
    ]
