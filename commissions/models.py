from django.db import models
from django.urls import reverse
from user_management.models import Profile

class Commission(models.Model):
    STATUS_CHOICES = (
        ('OPEN', 'Open'),
        ('FULL', 'Full'),
        ('COMP', 'Completed'),
        ('DISC', 'Discontinued'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='OPEN')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    # While unspecified in the specifications, it is impossible to check which
    # commissions the logged-in user has created without a foreign key to Profile
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("commissions:comm_detail", args=[self.id])


class Job(models.Model):
    STATUS_CHOICES = [
        ('1_OPEN', 'Open'),
        ('2_FULL', 'Full'),
    ]

    commission = models.ForeignKey(Commission, on_delete=models.CASCADE, related_name="jobs")
    role = models.CharField(max_length=255)
    manpower_required = models.PositiveIntegerField()
    status = models.CharField(max_length=6, choices=STATUS_CHOICES, default='1_OPEN')

    class Meta:
        ordering = ['status', '-manpower_required', 'role']

    def __str__(self):
        return self.role


class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('1_PEND', 'Pending'),
        ('2_ACPT', 'Accepted'),
        ('3_RJCT', 'Rejected'),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    applicant = models.ForeignKey(Profile, on_delete=models.CASCADE)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='1_PEND')
    applied_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['status', '-applied_on']

    def __str__(self):
        return f"{self.job} - {self.applicant}"
