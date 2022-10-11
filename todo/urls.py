from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('projects', views.ProjectViewSet, basename='projects')
router.register('tags', views.TagViewSet, basename='tags')
router.register('tasks', views.TaskViewSet, basename='tasks')

app_name = 'todo'

urlpatterns = [
    path('', include(router.urls)),
]
