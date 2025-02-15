from django.db import models
from django.contrib.auth.models import AbstractUser



# Creating the CustomUser class so we can have different kinds of users on the platform
#This class has 3 Children (investor,gamer,seller)
class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('investor', 'Investor'),
        ('gamer', 'Gamer'),
        ('seller', 'Seller'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
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


################################################################
# Seller Properties ->



class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    online_shop = models.ForeignKey('OnlineShop', related_name='products', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class OnlineShop(models.Model):

    name = models.CharField(max_length=100)
    url = models.URLField()
    description = models.TextField()
    seller = models.ForeignKey('Seller', on_delete=models.CASCADE)
    customer = models.CharField(max_length=100, default=None)
    sales = models.FloatField(default=0.00)
    logo = models.ImageField(default=None)


    def __str__(self):
        return f"{self.name} - {self.description}"




###############################################################
#Gamer Properties ->
class Level(models.Model):
    user = models.OneToOneField(Gamer, on_delete=models.CASCADE)
    level =models.IntegerField(default=1)

    def __str__(self):
        return self.user.username


class Points(models.Model):
    user = models.OneToOneField(Gamer, on_delete=models.CASCADE)
    points =models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

###############################################################
#Investor Properties ->

#Todo : update the properties of Investor class
