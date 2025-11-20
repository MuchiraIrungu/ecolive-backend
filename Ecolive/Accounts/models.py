from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


USERS = (
    ('admin', 'Admin'),
    ('investor', 'Investor'),
    ('farmer','Farmer')
)

STATUS = (
    ('active','Active'),
    ('pending', 'Pending'),
    ('Inactive','inactive'),
    ('producing','Producing')
)

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, max_length=255)
    role = models.CharField(max_length=12, choices=USERS, default='investor')
    wallet_address = models.CharField(max_length=100, null=True, blank=True)  # Hedera account ID
    
    USERNAME_FIELD = 'email'  # Use email for login instead of username
    REQUIRED_FIELDS = [] 

    objects = CustomUserManager()
    
    def __str__(self):
        return f"{self.email} ({self.role})"

# ---------------------------
# Hive and tokenization
# ---------------------------
class Hive(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    farmer = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, limit_choices_to={'role':'farmer'})
    status = models.CharField(max_length=50,choices=STATUS, default='active') # active, maintenance, producing
    pollination_percent = models.FloatField(default=0.0)
    honey_yield = models.FloatField(default=0.0)
    token_id = models.CharField(max_length=100, blank=True, null=True) # Hedera Token ID


# ---------------------------
# Investor investments
# ---------------------------
class Investment(models.Model):
    investor = models.ForeignKey('User', on_delete=models.CASCADE, limit_choices_to={'role':'investor'})
    hive = models.ForeignKey('Hive', on_delete=models.CASCADE)
    amount_invested = models.DecimalField(max_digits=12, decimal_places=2)
    token_id = models.CharField(max_length=100) # HTS token assigned
    date_created = models.DateTimeField(auto_now_add=True)
    simulated_payment_confirmed = models.BooleanField(default=False)


# ---------------------------
# Consensus / Hive Events
# ---------------------------
class HiveEvent(models.Model):
    hive = models.ForeignKey('Hive', on_delete=models.CASCADE)
    message = models.TextField()
    hedera_consensus_timestamp = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)


# Create your models here.
