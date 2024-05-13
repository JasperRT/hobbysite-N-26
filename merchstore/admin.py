from django.contrib import admin
from .models import ProductType, Product, Transaction


class ProductTypeAdmin(admin.ModelAdmin):
    model = ProductType

    search_fields = ('name',)
    list_display = ('id', 'name',)


class ProductAdmin(admin.ModelAdmin):
    model = Product

    search_fields = ('name',)
    list_display = ('id', 'name', 'product_type', 'owner',
                     'price', 'stock', 'status')


class TransactionAdmin(admin.ModelAdmin):
    model = Transaction

    search_fields = ('buyer',)
    list_display = ('id', 'buyer', 'product', 'amount',
                     'status', 'created_on')

admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Transaction, TransactionAdmin)
