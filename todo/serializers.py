from rest_framework import serializers

from .models import Project, Tag, Task, Change


class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Project
        fields = ('id', 'owner', 'title', 'description', 'deadline_date', 'deadline_time', 'created_at', 'updated_at')
        extra_kwargs = {'read_only_fields': ('owner', 'created_at', 'updated_at')}


class TagSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Tag
        fields = ('id', 'owner', 'title')
        extra_kwargs = {'read_only_fields': ('owner',)}


class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Task
        fields = (
            'id', 'parent', 'owner', 'title', 'description', 'deadline_date', 'deadline_time', 'completed',
            'occurrence_minutes', 'last_occurrence', 'priority', 'tags', 'reminder_minutes', 'project',
            'created_at', 'updated_at')
        extra_kwargs = {'read_only_fields': ('id', 'owner', 'created_at', 'updated_at')}


class ChangeSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()

    class Meta:
        model = Change
        fields = ('action', 'change_id', 'content_type', 'object_id', 'content')

    @staticmethod
    def get_content(obj: Change):
        if obj.content_type == Change.PROJECT:
            try:
                return ProjectSerializer(Project.objects.get(id=obj.object_id)).data
            except Project.DoesNotExist:
                return {}
        elif obj.content_type == Change.TASK:
            try:
                return TaskSerializer(Task.objects.get(id=obj.object_id)).data
            except Task.DoesNotExist:
                return {}
        elif obj.content_type == Change.TAG:
            try:
                return TagSerializer(Tag.objects.get(id=obj.object_id)).data
            except Tag.DoesNotExist:
                return {}
