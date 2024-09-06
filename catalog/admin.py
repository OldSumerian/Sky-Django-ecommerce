from django.contrib import admin
from catalog.models import Category, Product, ProductVersion


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "category")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "category")
    list_filter = ("category",)
    search_fields = (
        "name",
        "description",
    )

@admin.register(ProductVersion)
class ProductVersionAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "version_number", "version_name", "is_current")
    list_filter = ("product", "is_current")
    search_fields = (
        "product__name",
        "version_name",
    )

