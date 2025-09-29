import nested_admin
from django.contrib import admin
from .models import Anime, Category, Season, Episode

# 🔥 Episode inline
class EpisodeInline(nested_admin.NestedTabularInline):
    model = Episode
    extra = 1
    ordering = ("episode_number",)

# 🔥 Season inline (Episode bilan nested)
class SeasonInline(nested_admin.NestedTabularInline):
    model = Season
    inlines = [EpisodeInline]  # nested Episode
    extra = 1
    ordering = ("season_number",)

# 🔥 Anime admin (Season → Episode nested)
@admin.register(Anime)
class AnimeAdmin(nested_admin.NestedModelAdmin):
    list_display = ("id", "title", "slug", "get_categories", "created_at")  # ⚡ ManyToMany ni method orqali ko'rsatish
    list_filter = ("category", "created_at")
    list_display_links = ("title",)
    search_fields = ("title", "director", "genre")
    inlines = [SeasonInline]
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("category",)  # ⚡ category ni multi-select qilish

    def get_categories(self, obj):
        return ", ".join([c.name for c in obj.category.all()])
    get_categories.short_description = "Categories"

# 🔥 Category admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    list_display_links = ("name",)
