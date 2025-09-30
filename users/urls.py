from django.urls import path
from .views import RegisterView, UserView, admin_stats  # ✅ admin_stats ni import qilamiz
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("me/", UserView.as_view(), name="user-detail"),

    # 🔥 Admin statistikasi uchun
    path("admin-stats/", admin_stats, name="admin-stats"),
]
