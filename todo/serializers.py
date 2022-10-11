from django.utils import timezone
from rest_framework import serializers

from .models import Project, Tag, Task


class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Project
        fields = ('id', 'owner', 'title', 'description', 'deadline', 'created_at', 'updated_at')
        extra_kwargs = {'read_only_fields': ('id', 'owner', 'created_at', 'updated_at')}


class TagSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Tag
        fields = ('id', 'owner', 'title')
        extra_kwargs = {'read_only_fields': ('id', 'owner')}


class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Task
        fields = (
            'id', 'owner', 'title', 'description', 'deadline', 'completed', 'next_occurrence', 'last_occurrence',
            'priority', 'tags', 'reminder_minutes', 'project', 'created_at', 'updated_at')
        extra_kwargs = {'read_only_fields': ('id', 'owner', 'created_at', 'updated_at')}
