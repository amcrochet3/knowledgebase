# Generated by Django 4.2.7 on 2024-02-21 17:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("people_depot", "0004_alter_organization_id_alter_practicearea_id"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="organization",
            options={"ordering": ["name"]},
        ),
    ]
