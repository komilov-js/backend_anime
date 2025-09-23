from django.contrib import admin
from .models import Anime, Category, Episode

class EpisodeInline(admin.TabularInline):
    model = Episode
    extra = 1
    ordering = ("episode_number",)

@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "slug", "category", "created_at")
    list_filter = ("category", "created_at")
    list_display_links = ("title",) 
    search_fields = ("title", "description", "director", "studio", "genre")
    inlines = [EpisodeInline]
    # ⚡ prepopulated_fields shunchaki yangi qo'shishda avtomatik slug hosil qiladi
    prepopulated_fields = {"slug": ("title",)}
    # slug ham tahrirlashga ruxsat beriladi (readonly qilinmagan)
    readonly_fields = ()  # bo‘sh, hech narsa readonly emas

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ()  # hech narsa readonly emas
