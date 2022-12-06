from django.contrib import admin

from .models import Change, Project, Tag, Task, Shared


@admin.register(Change)
class ChangeAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'action', 'change_id', 'content_type', 'object_id')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'deadline_date', 'deadline_time', 'created_at', 'updated_at')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'id', 'completed')


@admin.register(Shared)
class SharedAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'shared_with', 'content_type', 'object_id')
