from django.db import models
from django.urls import reverse

class ProductType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # "Temporary" URL, product types are not actually accessible
        # because the model does not have a corresponding URL in
        # merchstore/urls.py, no view function in merchstore/views.py,
        # and no template in the merchstore/templates/merchstore folder.
        return "itemtype/" + self.id

class Product(models.Model):
    name = models.CharField(max_length=255)
    product_type = models.ForeignKey(ProductType, null=True, on_delete=models.SET_NULL)
    description = models.TextField()
    # Arbitrary max_digits; we assume that no price in the merch store costs more than 1M.
    price = models.DecimalField(max_digits=9, decimal_places = 2)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("merchstore:product_detail", args=[self.id])
