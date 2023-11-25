# todo: return authors
import uuid
from django.db import models
from django.db.models.constraints import UniqueConstraint
from django.contrib import admin


class AbstractBaseModel(models.Model):
    """
    Base abstract model, that has `uuid` instead of `uuid` and included `created_at`, `updated_at` fields.
    """
    
    created_at = models.DateTimeField("Created at", auto_now_add=True)
    updated_at = models.DateTimeField("Updated at", auto_now=True)

    class Meta:
        abstract = True



class AbstractBaseModelUuid(AbstractBaseModel):
    """
    Base abstract model, that has `uuid` instead of `uuid` and included `created_at`, `updated_at` fields.
    """

    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    
    created_at = models.DateTimeField("Created at", auto_now_add=True)
    updated_at = models.DateTimeField("Updated at", auto_now=True)

    class Meta:
        abstract = True

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.uuid}>"


class AbstractBaseModelId(AbstractBaseModel):
    """
    Base abstract model, that has `uuid` instead of `uuid` and included `created_at`, `updated_at` fields.
    """

    id = models.BigAutoField(primary_key=True)
    
    created_at = models.DateTimeField("Created at", auto_now_add=True)
    updated_at = models.DateTimeField("Updated at", auto_now=True)

    class Meta:
        abstract = True

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.uuid}>"



class Gdoc(AbstractBaseModelUuid):
    google_uuid = models.CharField(max_length=100, unique=True, blank=False, default="")
    title = models.CharField(max_length=70, blank=False, default="")
    description = models.CharField(max_length=200, blank=False, default="")
    slug = models.CharField(max_length=200, blank=False, default="")
    active = models.BooleanField(blank=False, default=False)
    phase = models.ForeignKey("Phase", on_delete=models.PROTECT, blank=False)
    published = models.BooleanField(default=False)
    practiceAreas = models.ManyToManyField("PracticeArea", blank=True)
    programAreas = models.ManyToManyField("ProgramArea", blank=True)
    tools = models.ManyToManyField("Tool", blank=True)
    technologies = models.ManyToManyField("Technology", blank=True)

    class Meta:
        unique_together = (
            "slug",
            "phase",
        )

    def to_json(self):
        return {
            "uuid": self.uuid,
            "google_uuid": self.google_uuid,
            "title": self.title,
            "description": self.description,
            "slug": self.slug,
            "published": self.published,
            "practiceAreas": [pa.name for pa in self.practiceAreas.all()],
            "programAreas": [pa.name for pa in self.programAreas.all()],
            "tools": [t.name for t in self.tools.all()],
            "technologies": [t.name for t in self.technologies.all()],
        }

    def __str__(self):
        return self.title + "(" + self.slug + ") " + self.phase.name




class Author(AbstractBaseModelUuid):
    name = models.CharField(
        max_length=70,
        blank=False,
        unique=True,
    )
    email = models.EmailField(
        max_length=70,
        blank=False,
        unique=True,
    )

    def __str__(self):
        return self.name


class GdocAuthor(AbstractBaseModelUuid):
    gdoc = models.ForeignKey(Gdoc, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, default="author")

    class Meta:
        unique_together = (
            "gdoc",
            "author",
        )

    def __str__(self):
        return self.gdoc.__str__() + " / " + self.author.__str__()


class GdocAuthorInline(admin.TabularInline):
    model = GdocAuthor
    extra = 5


class GdocAdmin(admin.ModelAdmin):
    inlines = [GdocAuthorInline]
    list_display = ("title", "slug", "phase", "published")
    list_filter = ["phase", "published"]
    search_fields = ["title", "description"]
    prepopulated_fields = {"slug": ("title",)}


class AuthorAdmin(admin.ModelAdmin):
    inlines = [GdocAuthorInline]
    list_display = ("name", "email")
    search_fields = ["name", "email"]


class PracticeArea(AbstractBaseModelId):
    name = models.CharField(
        max_length=70,
        blank=False,
        unique=True,
    )

    def __str__(self):
        return self.name

class ProgramArea(AbstractBaseModelId):
    name = models.CharField(
        max_length=70,
        blank=False,
        unique=True,
    )
    description = models.TextField(blank=True)
    image = models.URLField(blank=True)
        
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Phase(AbstractBaseModelUuid):
    name = models.CharField(
        max_length=70,
        blank=False,
        unique=True,
    )

    def __str__(self):
        return self.name


class Technology(AbstractBaseModelUuid):
    name = models.CharField(
        max_length=70,
        blank=False,
        unique=True,
    )

    def __str__(self):
        return self.name


class Tool(AbstractBaseModelUuid):
    name = models.CharField(
        max_length=70,
        blank=False,
        unique=True,
    )

    def __str__(self):
        return self.name