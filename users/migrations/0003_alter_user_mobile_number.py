# Generated by Django 5.2 on 2025-06-12 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_alter_user_username"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="mobile_number",
            field=models.CharField(max_length=10),
        ),
    ]
