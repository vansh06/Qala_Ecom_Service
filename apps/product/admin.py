from django.contrib import admin
from .models import Product, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'level', 'parent_category']
    list_filter = ['level']
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'brand', 'category', 'price', 'discount_percent', 'discounted_price', 'stock_status', 'quantity']
    list_filter = ['stock_status', 'brand', 'category']
    search_fields = ['title', 'sq_id', 'brand']
    readonly_fields = ['created_at', 'updated_at']
