from rest_framework import viewsets, filters, permissions
from rest_framework.exceptions import ValidationError
from .models import Anime, Category, SavedAnime
from .serializers import (
    AnimeSerializer,
    CategorySerializer,
    SavedAnimeSerializer,
)

# 🔥 Anime uchun ViewSet
class AnimeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Anime.objects.all().order_by("-created_at")
    serializer_class = AnimeSerializer
    lookup_field = "slug"
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]

    # 🔍 endi search Anime + Season + Episode bo‘yicha ham ishlaydi
    search_fields = [
        "title", "description", "director", "studio", "genre",
        "seasons__title", 
        "seasons__episodes__title", 
        "year"
    ]

    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.request.query_params.get("category")
        season_number = self.request.query_params.get("season")

        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        if season_number:
            queryset = queryset.filter(seasons__season_number=season_number).distinct()

        return queryset


# 🔥 Category uchun ViewSet
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"
    permission_classes = [permissions.AllowAny]


# 🔥 SavedAnime uchun ViewSet
class SavedAnimeViewSet(viewsets.ModelViewSet):
    serializer_class = SavedAnimeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SavedAnime.objects.filter(
            user=self.request.user
        ).select_related("anime")

    def perform_create(self, serializer):
        anime = serializer.validated_data.get("anime")  # SlugRelatedField orqali keladi

        # Agar foydalanuvchi shu anime’ni allaqachon saqlagan bo‘lsa
        if SavedAnime.objects.filter(user=self.request.user, anime=anime).exists():
            raise ValidationError("Siz bu animeni allaqachon saqlagansiz!")

        # Saqlash
        serializer.save(user=self.request.user, anime=anime)

