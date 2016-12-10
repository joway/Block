from rest_framework.permissions import BasePermission

from social.models import SocialAccount


def check_permission(permission_classes, self, request, obj=None):
    #  !!! permission_class must a tuple !!! such like (a,)
    #  self = Class ViewSet self
    self.permission_classes = permission_classes
    if obj is not None:
        self.check_object_permissions(request, obj)
    self.check_permissions(request)


class IsBound(BasePermission):
    def has_permission(self, request, view):
        return SocialAccount.objects.filter(access_token=request.POST['access_token'])


class IsAdminOrSelf(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_object_permission(self, request, view, obj):
        return request.method in [
            "OPTIONS"] or request.user.is_superuser or request.user == obj
