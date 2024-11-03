from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    COMPANY_CHOICES = [
        ('company1', 'Company 1'),
        ('company2', 'Company 2'),
    ]
    company = models.CharField(max_length=20, choices=COMPANY_CHOICES)

    def __str__(self):
        return f"{self.user.username} ({self.company})"
