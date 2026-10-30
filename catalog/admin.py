from django.contrib import admin
from .models import Product, Category, Review, Order


# ---------------- PRODUCT ----------------

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'price',
        'is_published',
        'category',
        'created_at',
    )

    list_filter = ('is_published', 'category')
    search_fields = ('title',)
    readonly_fields = ('slug', 'created_at', 'updated_at')

    fields = (
        'title',
        'slug',
        'category',
        'short_desc',
        'description',
        'price',
        'is_published',
        'image',
        'created_at',
        'updated_at',
    )


# ---------------- CATEGORY ----------------

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    search_fields = ('title',)
    readonly_fields = ('slug', 'created_at', 'updated_at')


# ---------------- REVIEW ----------------

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'rating', 'created_at')
    list_filter = ('rating',)
    search_fields = ('name', 'product__title')


# ---------------- ORDER ----------------

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('material_price', 'created_at')
    fields = ('material_price',)

