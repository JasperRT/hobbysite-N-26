from django.shortcuts import render
from .models import ProductType, Product

def products_list(request):
    products = Product.objects.all().order_by('name')
    ctx = {"products": products}
    return render(request, "merchstore/products_list.html", ctx)

def product_detail(request, id):
    product = Product.objects.get(id__exact=id)
    ctx = {"product": product}
    return render(request, "merchstore/product_detail.html", ctx)
