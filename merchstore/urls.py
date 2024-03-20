from django.urls import path
from .views import products_list, product_detail

urlpatterns = [
    path('merchstore/items', products_list, name="products_list"),
    path('merchstore/<int:id>', product_detail, name="product_detail"),
]

app_name = 'merchstore'
