# Generated by Django 5.0.4 on 2024-05-06 10:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("comix", "0011_posters"),
    ]

    operations = [
        migrations.AddField(
            model_name="genre",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="comix/images/"),
        ),
    ]
