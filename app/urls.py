from rest_framework.routers import DefaultRouter
from .views import AnimeViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r"animes", AnimeViewSet, basename="animes")
router.register(r"categories", CategoryViewSet, basename="categories")

urlpatterns = router.urls
