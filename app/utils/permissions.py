from rest_framework.permissions import BasePermission
from profile.models import Experience


class IsOwner(BasePermission):
    """
    Object Level permissions that will only allow REST API users to see their own objects
    """

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user
