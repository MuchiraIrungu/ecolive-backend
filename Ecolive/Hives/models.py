# hives/models.py
from django.db import models
from farmers.models import Farmer
from accounts.models import User

class Hive(models.Model):
    hive_id = models.CharField(max_length=20, unique=True)  # e.g., HVE-001
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='hives')
    location = models.CharField(max_length=100)
    price_hbar = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(
        max_length=10,
        choices=[('available', 'Available'), ('sold', 'Sold')],
        default='available'
    )
    token_id = models.CharField(max_length=50, blank=True, null=True)
    nft_serial = models.IntegerField(blank=True, null=True)
    investor = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='owned_hives'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.hive_id} - {self.location}"

class HiveUpdate(models.Model):
    hive = models.ForeignKey(Hive, on_delete=models.CASCADE, related_name='updates')
    honey_kg = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    health = models.CharField(max_length=20)
    photo = models.ImageField(upload_to='updates/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Update for {self.hive.hive_id} at {self.timestamp}"