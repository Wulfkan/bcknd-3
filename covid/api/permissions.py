from rest_framework.permissions import BasePermission

class IsAdminUserCustom(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)
    
class IsMedicoUser(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and not request.user.is_staff and hasattr(request.user, 'medico'))