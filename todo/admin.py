from django.contrib import admin

from .models import Change, Project, Tag, Task


@admin.register(Change)
class ChangeAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'action', 'change_id', 'content_type', 'object_id')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'id', 'deadline', 'created_at', 'updated_at')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'id')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'id', 'deadline', 'completed')
