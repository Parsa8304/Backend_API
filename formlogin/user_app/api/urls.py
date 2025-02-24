from django.urls import path , include
from .views import registration_view , logout_view
from rest_framework_simplejwt.views import TokenObtainPairView , TokenRefreshView


urlpatterns = [

    path('register/', registration_view, name='register'),
    path( 'login/', TokenObtainPairView.as_view(),name = 'token_obtain_pair'),
    path( 'login/refresh', TokenRefreshView.as_view(),name = 'token_refresh'),
    path( 'logout', logout_view , name = 'logout')

]