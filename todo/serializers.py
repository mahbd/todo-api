from rest_framework import serializers

from .models import Project, Tag, Task


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'title', 'description', 'deadline', 'created_at', 'updated_at')
        kwargs = {'read_only_fields': ('id', 'created_at', 'updated_at')}


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'title')
        kwargs = {'read_only_fields': ('id',)}