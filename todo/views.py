from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Project, Tag, Task, Change, Shared
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


class ChangeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = todo_ss.ChangeSerializer
    http_method_names = methods_excluding_put
    permission_classes = [IsAuthenticated]
    lookup_field = 'change_id'

    def get_queryset(self):
        return Change.objects.filter(owner=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def last_id(self, request):
        return Response({'last_id': Change.objects.get_last_id(self.request.user)})


class SharedViewSet(viewsets.ModelViewSet):
    serializer_class = todo_ss.SharedSerializer
    http_method_names = methods_excluding_put
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # check queryset with-me
        if self.request.query_params.get('with-me', 'false') == 'true':
            return Shared.objects.filter(user=self.request.user)
        return Shared.objects.filter(owner=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def tasks(self, request):
        tasks = set()
        if request.query_params.get('with-me', 'false') == 'true':
            queryset = Shared.objects.filter(shared_with=self.request.user)
        else:
            queryset = Shared.objects.filter(owner=self.request.user)

        for shared in queryset:
            if shared.content_type == Shared.PROJECT:
                tasks.update(Task.objects.filter(project=shared.object_id))
            elif shared.content_type == Shared.TASK:
                tasks.add(Task.objects.get(id=shared.object_id))
            elif shared.content_type == Shared.TAG:
                tasks.update(Task.objects.filter(tags=shared.object_id))
        return Response({
            'count': len(tasks),
            'results': todo_ss.TaskSerializer(tasks, many=True).data
        })
