from django.db import models
from django.urls import reverse

class Commission(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    people_req = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("commissions:comm_detail", args=[self.id])

class Comment(models.Model):
    commission = models.ForeignKey(Commission, on_delete=models.CASCADE)
    entry = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.commission)

    def get_absolute_url(self):
        # "Temporary" URL, comments are not actually directly accessible
        # because the model does not have a view function in commissions/views.py
        # and no template in the commissions/templates/commissions folder.
        return "commissions/comment/" + self.id
