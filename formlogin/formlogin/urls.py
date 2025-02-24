from django.contrib import admin
from django.urls import path , include
from rest_framework_simplejwt.views import TokenObtainPairView , TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('formlogin_app.api.urls')),

    #urls for login and registration
    path('accounts/' , include('user_app.api.urls')),

]
