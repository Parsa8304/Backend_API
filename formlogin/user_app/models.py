from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('investor', 'Investor'),
        ('gamer', 'Gamer'),
        ('seller', 'Seller'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    password = models.CharField(max_length=128)
    def __str__(self):
        return self.username

#################################################
# All children classes are defined below->

class Seller(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type': 'seller'})

    def __str__(self):
        return f"{self.user.username} - {self.user.user_type}"


class Investor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type': 'investor'})
    investment = models.DecimalField(max_digits=10, decimal_places=2 ,default=0)
    def __str__(self):
        return f"{self.user.username} - {self.user.user_type}"
    portfolio = models.DecimalField(max_digits=10, decimal_places=2 ,default=0)

    def __str__(self):
        return f"{self.user.username} - {self.user.user_type}"


class Gamer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type': 'gamer'})

    def __str__(self):
        return f"{self.user.username} - {self.user.user_type}"
