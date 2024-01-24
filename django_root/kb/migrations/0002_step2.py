# Generated by Django 4.2.7 on 2024-01-15 21:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("people_depot", "0001_initial"),
        ("kb", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Phase",
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
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created at"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Updated at"),
                ),
                ("name", models.CharField(max_length=70, unique=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="TopicArea",
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
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created at"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Updated at"),
                ),
                ("name", models.CharField(max_length=70, unique=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="AssetGroup",
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
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created at"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Updated at"),
                ),
                ("title", models.CharField(default="", max_length=70)),
                ("description", models.CharField(default="", max_length=200)),
                (
                    "practiceAreas",
                    models.ManyToManyField(blank=True, to="people_depot.practicearea"),
                ),
                ("tools", models.ManyToManyField(blank=True, to="people_depot.tool")),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Asset",
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
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created at"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Updated at"),
                ),
                (
                    "google_id",
                    models.CharField(default="", max_length=100, unique=True),
                ),
                ("title", models.CharField(default="", max_length=70)),
                ("description", models.CharField(default="", max_length=200)),
                ("slug", models.CharField(default="", max_length=200)),
                ("active", models.BooleanField(default=False)),
                ("published", models.BooleanField(default=False)),
                (
                    "phase",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="kb.phase"
                    ),
                ),
            ],
            options={
                "unique_together": {("slug", "phase")},
            },
        ),
        migrations.CreateModel(
            name="AssetUser",
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
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created at"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Updated at"),
                ),
                ("role", models.CharField(default="user", max_length=20)),
                (
                    "asset",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="kb.asset"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "unique_together": {("asset", "user")},
            },
        ),
    ]