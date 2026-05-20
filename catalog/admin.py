from django.contrib import admin
from .models import Category, Product, ProductImage, Review, Order


class ProductImageInline(admin.TabularInline):
    model = ProductImage
extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
prepopulated_fields = {"slug": ("title",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'is_published')
list_filter = ('category', 'is_published')
search_fields = ('title', 'short_desc')
inlines = [ProductImageInline]
prepopulated_fields = {"slug": ("title",)}


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'rating', 'created_at')
list_filter = ('rating',)
search_fields = ('name', 'text')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'product', 'status', 'created_at')
list_filter = ('status',)
search_fields = ('name', 'phone', 'comment')
