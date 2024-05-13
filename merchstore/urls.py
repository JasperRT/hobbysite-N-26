from django.urls import path
from .views import products_list, product_detail, product_create, product_update, cart_view, transactions_list


urlpatterns = [
    path('items/', products_list, name="products_list"),
    path('item/<int:id>/', product_detail, name="product_detail"),
    path('item/add/', product_create, name='product_create'),
    path('item/<int:id>/edit/', product_update, name='product_update'),
    path('cart/', cart_view, name='cart_view'),
    path('transactions/', transactions_list, name='transaction_list'),
]

app_name = 'merchstore'
