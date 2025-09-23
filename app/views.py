from rest_framework import viewsets, filters
from .models import Anime, Category
from .serializers import AnimeSerializer, CategorySerializer
from rest_framework.permissions import AllowAny


class AnimeViewSet(viewsets.ReadOnlyModelViewSet):  # faqat GET ishlaydi
    queryset = Anime.objects.all().order_by("-created_at")
    serializer_class = AnimeSerializer
    lookup_field = "slug"
    permission_classes = [AllowAny]   # Hamma ko‘ra oladi
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.request.query_params.get("category")
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        return queryset


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):  # faqat GET ishlaydi
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"
    permission_classes = [AllowAny]   # Hamma ko‘ra oladi
