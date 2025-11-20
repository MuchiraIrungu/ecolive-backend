from django.db import models
from Accounts.models import User

class Farmer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='farmer_profile')
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, unique=True)
    mpesa_number = models.CharField(max_length=15)

    def __str__(self):
        return self.full_name