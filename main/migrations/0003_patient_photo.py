# Generated by Django 4.2.16 on 2024-09-16 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0002_alter_appoint_options_alter_doctor_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="patient",
            name="photo",
            field=models.ImageField(blank=True, null=True, upload_to="patient/"),
        ),
    ]
