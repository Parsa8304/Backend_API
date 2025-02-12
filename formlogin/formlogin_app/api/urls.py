from django.urls import path
from .views import *

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path( 'register/', UserCreateView.as_view(), name='register'),
    path('seller/', SellerListCreateView.as_view(), name='seller')
]