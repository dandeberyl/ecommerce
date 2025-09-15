from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "price")
    list_filter = ("category",)
    search_fields = ("name", "description")


    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height:50px; object-fit: cover;" />', obj.image.url)
        return "No Image"

    image_preview.short_description = "Image"


