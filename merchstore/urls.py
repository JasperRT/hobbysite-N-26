from django.urls import path
from .views import products_list, product_detail

urlpatterns = [
    path('items', products_list, name="products_list"),
    path('item/<int:id>', product_detail, name="product_detail"),
]

app_name = 'merchstore'
