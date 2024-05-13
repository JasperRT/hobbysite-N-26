from django import forms
from .models import Product, Transaction


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'owner', 'product_type', 'description', 'price', 'stock', 'status')
        widgets = {
            'owner': forms.Select(attrs={
                "style": "pointer-events: none; background-color : #CCCCCC",
                "tabindex": "-1",
        })
        }


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('amount',)
