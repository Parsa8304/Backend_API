from rest_framework.throttling import UserRateThrottle, AnonRateThrottle



class CustomUserRateThrottle(UserRateThrottle):
       scope = 'seller'
       