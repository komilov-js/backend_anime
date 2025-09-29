from django.db import models
from django.utils.text import slugify
from users.models import User  # boshqa appdagi User model

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
    category = models.ManyToManyField(Category, blank=True, related_name="animes")  # ⚡ManyToMany
    anime_url = models.URLField(blank=True, null=True)
    anime_file = models.FileField(upload_to="animes/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    yosh_chegara = models.CharField(max_length=10, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:255]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Season(models.Model):
    anime = models.ForeignKey(Anime, related_name="seasons", on_delete=models.CASCADE)
    season_number = models.PositiveIntegerField()
    title = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["season_number"]
        unique_together = ("anime", "season_number")

    def __str__(self):
        return f"{self.anime.title} - {self.season_number}-fasl"


class Episode(models.Model):
    season = models.ForeignKey(
        Season,
        related_name="episodes",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    title = models.CharField(max_length=255, blank=True)
    episode_number = models.PositiveIntegerField(blank=True, null=True)  # ⚡ null=True qo‘shdik
    video_url = models.CharField(max_length=255000, blank=True)
    video_file = models.FileField(upload_to="episodes/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["episode_number"]
        unique_together = ("season", "episode_number")

    def save(self, *args, **kwargs):
        # Agar yangi episode qo'shilsa va number berilmagan bo'lsa
        if self.episode_number is None:
            last_episode = Episode.objects.filter(season=self.season).order_by("-episode_number").first()
            if last_episode:
                self.episode_number = last_episode.episode_number + 1
            else:
                self.episode_number = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.season.anime.title} - {self.episode_number}-qism"

# 🔥 Saqlangan animelar (user-ga)
class SavedAnime(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="saved_animes")
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "anime")

    def __str__(self):
        return f"{self.user.username} - {self.anime.title}"
    