from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Project, Tag, Task
from . import serializers as todo_ss

methods_excluding_put = ['head', 'options', 'get', 'post', 'patch', 'delete']


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = todo_ss.ProjectSerializer
    http_method_names = methods_excluding_put
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = todo_ss.TagSerializer
    http_method_names = methods_excluding_put
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Tag.objects.filter(owner=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = todo_ss.TaskSerializer
    http_method_names = methods_excluding_put
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)
