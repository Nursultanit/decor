
import re
from decimal import Decimal, InvalidOperation
from urllib.parse import urlencode

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from rest_framework import generics

from .models import Product, Category, Review, Order
from .serializers import (
    ProductSerializer,
    CategorySerializer,
    ReviewSerializer,
    OrderSerializer,
)


# Главная страница
def home(request):
    products = Product.objects.filter(is_published=True)
    categories = Category.objects.all()

    return render(request, 'catalog/home.html', {
        'products': products,
        'categories': categories,
    })


# Товары по категории
def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(
        category=category,
        is_published=True,
    )
    categories = Category.objects.all()

    return render(request, 'catalog/category.html', {
        'category': category,
        'products': products,
        'categories': categories,
    })


# Оформление заказа и переход в WhatsApp
def create_order(request):
    products = Product.objects.filter(is_published=True)

    product_id = (
        request.GET.get('product')
        or request.POST.get('product')
    )

    product = None

    if product_id:
        product = get_object_or_404(
            Product,
            pk=product_id,
            is_published=True,
        )

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()
        comment = request.POST.get('comment', '').strip()
        area_text = request.POST.get('area', '').strip()

        if not product:
            messages.error(request, 'Выбери декор в каталоге.')

        elif not name:
            messages.error(request, 'Введи своё имя.')

        elif not re.fullmatch(r'[0-9+\s()\-]{9,20}', phone):
            messages.error(
                request,
                'Телефон должен содержать только цифры и символы + ( ) -.',
            )

        elif not area_text:
            messages.error(request, 'Укажи площадь в м².')

        else:
            try:
                area = Decimal(area_text.replace(',', '.'))
            except (InvalidOperation, ValueError):
                area = Decimal('0')

            if not area.is_finite() or area <= 0:
                messages.error(
                    request,
                    'Площадь должна быть больше нуля.',
                )

            elif product.price is None or product.price < 0:
                messages.error(
                    request,
                    'Проверь цену материала в каталоге.',
                )

            else:
                material_unit_price = product.price
                application_unit_price = (
                    product.application_price or Decimal('0')
                )

                if application_unit_price < 0:
                    messages.error(
                        request,
                        'Проверь цену нанесения в каталоге.',
                    )

                else:
                    material_total = material_unit_price * area
                    application_total = application_unit_price * area
                    total_price = material_total + application_total

                    # Сохраняем заказ в базе данных
                    order = Order.objects.create(
                        product=product,
                        name=name,
                        phone=phone,
                        address=address,
                        area=area,
                        service_type='both',
                        material_price=material_total,
                        application_price=application_total,
                        total_price=total_price,
                        comment=comment,
                    )

                    # Полный текст заказа
                    message = (
                        f'Здравствуйте! Новый заказ ART DECOR №{order.pk}\n\n'
                        f'Декор: {product.title}\n'
                        f'Услуга: Материал + нанесение\n'
                        f'Площадь: {area} м²\n'
                        f'Имя: {name}\n'
                        f'Телефон: {phone}\n'
                        f'Адрес: {address or "Не указан"}\n'
                        f'Комментарий: {comment or "Нет"}\n\n'
                        f'Материал: {material_total:.2f} сом\n'
                        f'Нанесение: {application_total:.2f} сом\n'
                        f'Итого: {total_price:.2f} сом'
                    )

                    # Кодируем сообщение для WhatsApp
                    whatsapp_url = (
                        'https://api.whatsapp.com/send?'
                        + urlencode({
                            'phone': '996706010902',
                            'text': message,
                        })
                    )

                    return redirect(whatsapp_url)

    return render(request, 'catalog/order.html', {
        'products': products,
        'product': product,
    })


# API: список опубликованных товаров
class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.filter(is_published=True)
    serializer_class = ProductSerializer


# API: товар по slug
class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_published=True)
    serializer_class = ProductSerializer
    lookup_field = 'slug'


# API: категории
class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# API: создание отзыва
class ReviewCreateAPIView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


# API: создание заказа
class OrderCreateAPIView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer





