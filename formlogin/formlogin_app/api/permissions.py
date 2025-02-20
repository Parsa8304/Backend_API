from rest_framework import permissions




class IsAdminOrRead(permissions.BasePermission):
    """
    Custom permission to only allow Admins to edit and read access for others.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.user_type == 'seller'


class IsInvestor(permissions.BasePermission):
    """
    Custom permission to only allow Investor to edit and read access for others.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated  and request.user.user_type == 'investor'


class IsGamer(permissions.BasePermission):
    """
      Custom permission to only allow Gamers to edit and read access for others.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'gamer'

class IsSellerOrRead(permissions.BasePermission):
    """
    Custom permission to only allow sellers to edit and read access for others.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.user_type == 'seller'

