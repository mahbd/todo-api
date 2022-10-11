from rest_framework import viewsets, permissions

from users.models import User
from users.serializers import UserSerializer, AdminUserSerializer


class UserPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated
                    and (request.user.is_staff or request.user.id == obj.id))


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (UserPermission,)

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return AdminUserSerializer
        return UserSerializer
