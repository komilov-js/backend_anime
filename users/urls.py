from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, UserView, admin_stats  # ✅ admin_statsni shu yerda import qilamiz

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("me/", UserView.as_view(), name="user-detail"),
    path("admin-stats/", admin_stats, name="admin-stats"),  # ✅ admin stats endpoint
]
