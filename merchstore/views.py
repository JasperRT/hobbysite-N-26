from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Lower

from .models import Profile, Product, Transaction
from .forms import ProductForm, TransactionForm


def products_list(request):
    if request.user.is_authenticated:
        curr_profile = Profile.objects.get(user=request.user)
        user_products = Product.objects.filter(owner=curr_profile).order_by(Lower('name'))
        other_products = Product.objects.exclude(owner=curr_profile).order_by(Lower('name'))
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
            product.stock -= trans.amount
            product.save()
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
    else:
        return render(request, "merchstore/product_detail.html", ctx)


@login_required
def product_create(request):
    curr_profile = Profile.objects.get(user=request.user)
    prod_form = ProductForm(initial={'owner': curr_profile})
    if request.method == 'POST':
        prod_form = ProductForm(request.POST)
        if prod_form.is_valid():
            new_product = prod_form.save()
            return redirect('merchstore:product_detail', id=new_product.id)
    ctx = { "prod_form": prod_form }
    return render(request, "merchstore/product_create.html", ctx)


@login_required
def product_update(request, id):
    curr_profile = Profile.objects.get(user=request.user)
    product = Product.objects.get(id=id)
    prod_update_form = ProductForm(instance=product)
    if request.method == 'POST':
        prod_update_form = ProductForm(request.POST)
        if prod_update_form.is_valid():
            updated_prod = prod_update_form.save(commit=False)
            updated_prod.id = product.id
            if updated_prod.stock == 0:
                updated_prod.status = 'OUT'
            else:
                updated_prod.status = 'AVAIL'
            updated_prod.save()
            return redirect('merchstore:product_detail', id=updated_prod.id)
    ctx = { "curr_profile": curr_profile, "product": product, "prod_update_form": prod_update_form }
    return render(request, "merchstore/product_update.html", ctx)


@login_required
def cart_view(request):
    curr_profile = Profile.objects.get(user=request.user)
    user_purch = Transaction.objects.filter(buyer=curr_profile).order_by('-created_on')

    print(user_purch)

    parted_purch = {}

    for purchase in user_purch:
        owner = purchase.product.owner
        if owner not in parted_purch:
            parted_purch[owner] = []
        parted_purch[owner].append(purchase)

    ctx = { "curr_profile": curr_profile, "parted_purch": parted_purch }
    return render(request, "merchstore/cart_view.html", ctx)


@login_required
def transactions_list(request):
    curr_profile = Profile.objects.get(user=request.user)
    user_trans = Transaction.objects.filter(product__owner=curr_profile).order_by('-created_on')

    parted_trans = {}

    for transaction in user_trans:
        buyer = transaction.buyer
        if buyer not in parted_trans:
            parted_trans[buyer] = []
        parted_trans[buyer].append(transaction)

    ctx = {"curr_profile": curr_profile, "parted_trans": parted_trans}
    return render(request, "merchstore/transactions_list.html", ctx)
