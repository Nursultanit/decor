from django.urls import path
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from .models import Product, Category, Order
from .serializers import ProductSerializer, CategorySerializer, OrderSerializer

class ProductListAPI(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailAPI(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'

class CategoryListAPI(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class OrderCreateAPI(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

urlpatterns = [
    path('', ProductListAPI.as_view(), name='api_products'),
    path('', ProductDetailAPI.as_view(), name='api_product_detail'),
    path('', CategoryListAPI.as_view(), name='api_categories'),
    path('', OrderCreateAPI.as_view(), name='api_create_order'),
]
