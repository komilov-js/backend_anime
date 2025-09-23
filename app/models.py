from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Anime(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(blank=True)
    bg_image = models.URLField(blank=True, null=True)
    main_image = models.URLField(blank=True, null=True)
    director = models.CharField(max_length=255, blank=True, null=True)
    genre = models.CharField(max_length=25000, blank=True, null=True)
    year = models.CharField(max_length=255, blank=True, null=True)
    studio = models.CharField(max_length=255, blank=True, null=True)

    # 🔥 Category bilan bog‘laymiz
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="animes"
    )

    anime_url = models.URLField(blank=True, null=True)
    anime_file = models.FileField(upload_to="animes/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:255]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Episode(models.Model):
    anime = models.ForeignKey(
        Anime, related_name="episodes", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255, blank=True)
    episode_number = models.PositiveIntegerField()
    video_url = models.CharField(max_length=255000, blank=True)
    video_file = models.FileField(upload_to="episodes/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["episode_number"]
        unique_together = ("anime", "episode_number")

    def __str__(self):
        return f"{self.anime.title} - {self.episode_number}-qism"
