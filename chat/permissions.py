from rest_framework.permissions import BasePermission


class IsCurrentUser(BasePermission):
    message = 'Unauthorized Access, either your session has expired or you do not have proper permissions.'
    def has_permission(self, request, view):
        if(request.user.id == view.kwargs["pk"]):
            return True
        else:
            return False

