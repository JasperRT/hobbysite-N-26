from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import ProductType, Profile, Product
from .forms import TransactionForm

def products_list(request):
    if request.user.is_authenticated:
        curr_profile = Profile.objects.get(user=request.user)
        user_products = Product.objects.filter(owner=curr_profile).order_by('name')
        other_products = Product.objects.exclude(owner=curr_profile).order_by('name')
        ctx = { "user_products": user_products, "other_products": other_products }
    else:
        products = Product.objects.all().order_by('name')
        ctx = { "products": products }
    return render(request, "merchstore/products_list.html", ctx)

def product_detail(request, id):
    product = Product.objects.get(id=id)
    trans_form = TransactionForm()
    if request.user.is_authenticated:
        curr_profile = Profile.objects.get(user=request.user)
        ctx = { "product": product, "curr_profile": curr_profile }
    else:
        ctx = { "product": product, "trans_form": trans_form }
    if request.method == 'POST':
        trans_form = TransactionForm(request.POST)
        if trans_form.is_valid():
            temp_form = trans_form.save(commit=False)
            if request.user.is_authenticated:
                temp_form.buyer = curr_profile
                temp_form.product = product
                temp_form.status = "CART"
                temp_form.save()
                product.stock -= temp_form.amount
                product.save()
                return redirect('merchstore:cart_view')
            else:
                request.session['transaction_data'] = {
                    'product_id': product.id,
                    'amount': temp_form.amount,
                }
                return redirect('login')

    else:
        return render(request, "merchstore/product_detail.html", ctx)

@login_required
def product_create(request):
    return render(request, "merchstore/product_create.html", ctx)

@login_required
def product_update(request, id):
    product = Product.objects.get(id__exact=id)
    ctx = {"product": product}
    return render(request, "merchstore/product_update.html", ctx)

@login_required
def cart_view(request):
    return render(request, "merchstore/cart_view.html", ctx)

@login_required
def transactions_list(request):
    return render(request, "merchstore/transactions_list.html", ctx)
