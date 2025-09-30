# admin.py
from django.contrib import admin
from django.contrib.auth.models import User
from django.urls import path
from django.http import HttpResponse

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "is_staff")

# Custom statistik sahifa
class MyAdminSite(admin.AdminSite):
    site_header = "Mening Admin Panelim"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("stats/", self.admin_view(self.stats_view))
        ]
        return custom_urls + urls

    def stats_view(self, request):
        total_users = User.objects.count()
        return HttpResponse(f"<h1>Umumiy foydalanuvchilar soni: {total_users}</h1>")

admin_site = MyAdminSite(name="myadmin")
