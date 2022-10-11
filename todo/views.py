from rest_framework import viewsets

from .models import Project, Tag, Task
from . import serializers as todo_ss


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = todo_ss.ProjectSerializer
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = todo_ss.TagSerializer
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
