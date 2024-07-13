from django.contrib import admin
from blog.models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "published",)
    list_filter = ("published",)
    search_fields = (
        "title",
        "content",
    )
    actions = ["toggle_publish"]

    def toggle_publish(self, request, queryset):
        queryset.update(published=not queryset.first().published)
        self.message_user(request, f"{queryset.count()} стать{'' if queryset.count() == 1 else 'и'} были опубликованы." if queryset.first().published else f"{queryset.count()} стать{'' if queryset.count() == 1 else 'и'} были сняты с публикации.")
