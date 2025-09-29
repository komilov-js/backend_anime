from rest_framework import serializers
from .models import Anime, Episode, Category, Season, SavedAnime

class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = ["id", "title", "episode_number", "video_url", "video_file", "created_at"]

class SeasonSerializer(serializers.ModelSerializer):
    episodes = EpisodeSerializer(many=True, read_only=True)

    class Meta:
        model = Season
        fields = ["id", "season_number", "title", "created_at", "episodes"]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]

class AnimeSerializer(serializers.ModelSerializer):
    seasons = SeasonSerializer(many=True, read_only=True)
    category = serializers.SerializerMethodField()

    class Meta:
        model = Anime
        fields = [
            "id", "title", "slug", "description", "bg_image", "main_image",
            "director", "genre", "year", "studio", "anime_url", "anime_file",
            "category", "created_at", "seasons","yosh_chegara"
        ]

    def get_category(self, obj):
        return [{"id": c.id, "name": c.name, "slug": c.slug} for c in obj.category.all()]
    

class SavedAnimeSerializer(serializers.ModelSerializer):
    anime = AnimeSerializer(read_only=True)
    anime_slug = serializers.SlugRelatedField(
        queryset=Anime.objects.all(), slug_field='slug', source='anime', write_only=True
    )

    class Meta:
        model = SavedAnime
        fields = ["id", "user", "anime", "anime_slug", "created_at"]
        read_only_fields = ["user", "anime"]
