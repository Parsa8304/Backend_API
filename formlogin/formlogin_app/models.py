from django.db import models
from django.contrib.auth.models import AbstractUser
from user_app.models import Seller , Investor , Gamer , CustomUser



# Creating the CustomUser class so we can have different kinds of users on the platform
#This class has 3 Children (investor,gamer,seller)

################################################################
# Seller Properties ->

class Product(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    online_shop = models.ForeignKey('OnlineShop', related_name='products', on_delete=models.CASCADE)
    analytics = models.OneToOneField('ProductAnalytics', on_delete=models.CASCADE, null=True, blank=True, related_name='product_analytics')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_shop_link(self):
        return f'{self.online_shop.get_absolute_url()}/{self.title}'

class OnlineShop(models.Model):

    name = models.CharField(max_length=100)
    url = models.URLField()
    description = models.TextField()
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    # customer = models.CharField(max_length=100, default=None , null = True)
    sales = models.FloatField(default=0.00)
    logo = models.ImageField(upload_to='logo/',default=None)


    def __str__(self):
        return f"{self.name} - {self.description}"


class ProductAnalytics(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='analytics_data')
    views = models.IntegerField(default=0)
    clicks = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.title} Analytics"


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
#
class Tokens(models.Model):
    owner = models.ForeignKey(Gamer, on_delete=models.CASCADE)
    token_name = models.CharField(max_length=20)
    amount = models.FloatField(default=0)

    def __str__(self):
        return f"{self.owner.username} - {self.token_name}"



###############################################################
#Investor Properties ->




#Todo : update the properties of Investor class
