# catalog/views.py
from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from .forms import OrderForm

def product_list(request):
    products = Product.objects.all()
    return render(request, 'catalog/product_list.html', {'products': products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.product = product
            order.save()
            return render(request, 'catalog/order_success.html', {'product': product})
    else:
        form = OrderForm()

    return render(request, 'catalog/product_detail.html', {
        'product': product,
        'form': form
    })
