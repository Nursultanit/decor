from rest_framework import generics
from django.shortcuts import render, get_object_or_404

from .models import Product, Category, Review, Order

from .serializers import (
    ProductSerializer,
    CategorySerializer,
    ReviewSerializer,
    OrderSerializer
)


# 🏠 главная страница
def home(request):

    products = Product.objects.filter(is_published=True)
    categories = Category.objects.all()

    return render(request, 'catalog/home.html', {
        'products': products,
        'categories': categories
    })


# 📂 товары по категории
def category_products(request, slug):

    category = get_object_or_404(
        Category,
        slug=slug
    )

    products = Product.objects.filter(
        category=category,
        is_published=True
    )

    categories = Category.objects.all()

    return render(request, 'catalog/category.html', {
        'category': category,
        'products': products,
        'categories': categories
    })


# 📦 список товаров
class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.filter(is_published=True)
    serializer_class = ProductSerializer


# 🧾 страница товара
class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_published=True)
    serializer_class = ProductSerializer
    lookup_field = 'slug'


# 📂 категории
class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# ⭐ отзывы
class ReviewCreateAPIView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


# 📦 заказ
class OrderCreateAPIView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
