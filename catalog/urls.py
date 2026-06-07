from django.urls import path
from .views import (
    home,
    category_products,
    ProductListAPIView,
    ProductDetailAPIView,
    ReviewCreateAPIView,
    CategoryListAPIView,
    OrderCreateAPIView,
)

urlpatterns = [

    # сайт
    path('', home, name='home'),

    path(
        'category/<slug:slug>/',
        category_products,
        name='category'
    ),

    # API
    path('api/products/', ProductListAPIView.as_view()),
    path('api/products/<slug:slug>/', ProductDetailAPIView.as_view()),
    path('api/categories/', CategoryListAPIView.as_view()),
    path('api/reviews/', ReviewCreateAPIView.as_view()),
    path('api/orders/', OrderCreateAPIView.as_view()),
]