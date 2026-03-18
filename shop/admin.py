from django.contrib import admin
from .models import Product, Category, Manufacture

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "quantity", "category", "manufacture")
    list_filter = ("category", "manufacture")
    search_fields = ("name",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Manufacture)
class ManufactureAdmin(admin.ModelAdmin):
    list_display = ("name", "country")
    search_fields = ("name", "country")
