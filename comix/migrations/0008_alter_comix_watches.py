# Generated by Django 5.0.4 on 2024-04-27 18:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("comix", "0007_comix_watches_alter_comments_text_delete_watched"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comix",
            name="watches",
            field=models.PositiveIntegerField(default=1),
        ),
    ]
