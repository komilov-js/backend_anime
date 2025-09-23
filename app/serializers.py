from rest_framework import serializers
from .models import Anime, Episode, Category

class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = ["id", "title", "episode_number", "video_url", "video_file", "created_at"]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]

class AnimeSerializer(serializers.ModelSerializer):
    episodes = EpisodeSerializer(many=True, read_only=True)
    category = serializers.SerializerMethodField()  # shu qism o'zgardi

    class Meta:
        model = Anime
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "bg_image",
            "main_image",
            "director",
            "genre",
            "year",
            "studio",
            "anime_url",
            "anime_file",
            "category",
            "created_at",
            "episodes",
        ]

    def get_category(self, obj):
        if obj.category:
            return {
                "id": obj.category.id,
                "name": obj.category.name,
                "slug": obj.category.slug  # bu frontend uchun muhim
            }
        return None
