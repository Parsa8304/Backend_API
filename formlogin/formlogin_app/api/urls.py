from django.urls import path , include
from .views import *
from rest_framework.routers import DefaultRouter

#Todo : clean up the URL stuff



router = DefaultRouter()
router.register('Products', ProductViewSet)

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path( 'register/', UserCreateView.as_view(), name='register'),
    # path('seller/', SellerListCreateView.as_view(), name='seller')
    path( 'users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>', UserDetailView.as_view(), name='user-detail'),


    path('online-shops/', OnlineShopListView.as_view(), name='online-shop-list'),
    path('online-shops/create/', OnlineShopCreateView.as_view(), name='online-shop-create'),
    # path('products/', ProductListView.as_view(), name='product-list'),
    # path('products/create/', ProductCreateView.as_view(), name='product-create'),
    path("", include(router.urls)),

]