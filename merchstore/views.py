from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Profile, Product, Transaction
from .forms import ProductForm, TransactionForm


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
        if 'transaction_data' in request.session:
            trans_data = request.session.pop('transaction_data')
            trans = Transaction()
            trans.buyer = curr_profile
            trans.product = product
            trans.amount = trans_data['amount']
            trans.status = "CART"
            trans.save()
            return redirect('merchstore:cart_view')
        else:
            ctx = { "product": product, "curr_profile": curr_profile, "trans_form": trans_form }
    else:
        ctx = { "product": product, "trans_form": trans_form }
    if request.method == 'POST':
        trans_form = TransactionForm(request.POST)
        if trans_form.is_valid():
            temp_form = trans_form.save(commit=False)
            if product.stock >= temp_form.amount:
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
                        'amount': temp_form.amount
                    }
                    return redirect(f'/accounts/login/?next={request.path}')
    else:
        return render(request, "merchstore/product_detail.html", ctx)


@login_required
def product_create(request):
    curr_profile = Profile.objects.get(user=request.user)
    prod_form = ProductForm()
    prod_form.owner = curr_profile
    prod_form.fields['owner'].disabled = True
    if request.method == 'POST':
        prod_form = ProductForm(request.POST)
        if prod_form.is_valid():
            prod_form.save()
            return redirect('merchstore:product_detail', id=prod_form.id)
    ctx = { "prod_form": prod_form }
    return render(request, "merchstore/product_create.html", ctx)


@login_required
def product_update(request, id):
    product = Product.objects.get(id__exact=id)
    prod_update_form = ProductUpdateForm()
    if request.method == 'POST':
        prod_update_form = ProductUpdateForm(request.POST)
        if prod_form.is_valid():
            temp_form = prod_form.save(commit=False)
            temp_form.owner = curr_profile
            temp_form.save()
            return redirect('merchstore:product_detail', id=temp_form.id)
    ctx = { "prod_update_form": prod_update_form }
    return render(request, "merchstore/product_update.html", ctx)


@login_required
def cart_view(request):
    product = Product.objects.get(id=0)
    ctx = { "product": product }
    return render(request, "merchstore/cart_view.html", ctx)


@login_required
def transactions_list(request):
    return render(request, "merchstore/transactions_list.html", ctx)
