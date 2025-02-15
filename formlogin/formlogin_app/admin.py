from django.contrib import admin
from .models import CustomUser , OnlineShop ,Seller,Product
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Seller)
admin.site.register(OnlineShop)
admin.site.register(Product)
