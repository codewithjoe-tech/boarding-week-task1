from rest_framework.permissions import BasePermission
from rest_framework.request import Request







class IsEmailVerified(BasePermission):
    def has_permission(self, request: Request, view):
        user = request.user
        return user and user.is_authenticated and getattr(user, "is_email_verified", False)
