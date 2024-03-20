from django.contrib import admin
from .models import ProductType, Product

class ProductTypeAdmin(admin.ModelAdmin):
    model = ProductType

    search_fields = ('name', )

class ProductAdmin(admin.ModelAdmin):
    model = Product

    search_fields = ('name',)

admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(Product, ProductAdmin)
