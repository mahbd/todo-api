from rest_framework import viewsets

from .models import Project, Tag, Task
from . import serializers as todo_ss

methods_excluding_put = ['head', 'options', 'get', 'post', 'patch', 'delete']


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = todo_ss.ProjectSerializer
    http_method_names = methods_excluding_put


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = todo_ss.TagSerializer
    http_method_names = methods_excluding_put


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = todo_ss.TaskSerializer
    http_method_names = methods_excluding_put
