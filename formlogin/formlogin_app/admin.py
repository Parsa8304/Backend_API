from django.contrib import admin
from .models import CustomUser , OnlineShop ,Seller,Product , ProductAnalytics
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Seller)
admin.site.register(OnlineShop)
admin.site.register(Product)
admin.site.register(ProductAnalytics)
