from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('admin', 'Admin'),
        ('manager', 'Manager'),
    )
    COMPANY_CHOICES = (
        ('company1', 'Company 1'),
        ('company2', 'Company 2'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    company = models.CharField(max_length=10, choices=COMPANY_CHOICES)

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    company = models.CharField(max_length=10, choices=User.COMPANY_CHOICES)

    def __str__(self):
        return self.name