from django.db import models
from django.urls import reverse
from user_management.models import Profile

class ProductType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # "Temporary" URL, product types are not actually directly accessible
        # because the model does not have a view function in merchstore/views.py
        # and no template in the merchstore/templates/merchstore folder.
        return "merchstore/itemtype/" + self.id

class Product(models.Model):
    STATUS_CHOICES = (
        ('AVAIL', 'Available'),
        ('SALE', 'On Sale'),
        ('OUT', 'Out of Stock'),
    )

    name = models.CharField(max_length=255)
    product_type = models.ForeignKey(ProductType, null=True, on_delete=models.SET_NULL)
    description = models.TextField()
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    # Arbitrary max_digits; we assume that no price in the merch store costs more than 1M.
    price = models.DecimalField(max_digits=9, decimal_places=2)
    stock = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='AVAIL')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("merchstore:product_detail", args=[self.id])

class Transaction(models.Model):
    STATUS_CHOICES = (
        ('CART', 'On Cart'),
        ('TPAY', 'To Pay'),
        ('TSHIP', 'To Ship'),
        ('TRECEIVE', 'To Receive'),
        ('DELIVER', 'Delivered'),
    )

    buyer = models.ForeignKey(Profile, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    amount = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
