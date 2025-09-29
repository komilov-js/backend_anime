from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnimeViewSet, CategoryViewSet, SavedAnimeViewSet

router = DefaultRouter()
router.register(r'animes', AnimeViewSet, basename='anime')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'saved-animes', SavedAnimeViewSet, basename='saved_anime')

urlpatterns = [
    path('', include(router.urls)),
]
