from rest_framework import permissions



class IsInvestor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated  and request.user.user_type == 'investor'

class IsGamer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'gamer'

class IsSeller(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'seller'

