from django.urls import path , include
from .views import *
from rest_framework.routers import DefaultRouter




# replacing the url patterns with the router url design
# so it's more readable
######################################

router = DefaultRouter()
router.register('Products', ProductViewSet)
router.register('onlineshop', OnlineShopViewSet)
router.register('users', UserViewSet)
router.register('login', LoginViewSet, basename='login')


#######################################

urlpatterns = [
    path("", include(router.urls)),
    path('track-click/', TrackClickView.as_view(), name='track-click'),
    path('track-view/', TrackViewView.as_view(), name='track-view'),
]