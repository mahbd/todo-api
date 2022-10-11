from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework.test import RequestsClient

from .models import Project, Tag, Task

User = get_user_model()

c = RequestsClient()

S_URL = "http://testserver"


# ToDo: Add user based restrictions
class ProjectTestCase(TestCase):
    def setUp(self) -> None:
        self.api_url = S_URL + reverse("todo:projects-list")

    def test_create_project(self):
        response = c.post(self.api_url, {'title': 'test', 'description': 'test'})
        self.assertEqual(response.status_code, 201, msg=f'Project must be created {response.json()}')
        project = Project.objects.get(title='test')
        self.assertEqual(project.description, 'test', msg=f'Project description must be correct: {project.description}')

    def test_update_project(self):
        c.post(self.api_url, {'title': 'test', 'description': 'test'})
        project = Project.objects.get(title='test')
        response = c.patch(S_URL + reverse("todo:projects-detail", kwargs={'pk': project.id}),
                           json={'description': 'test2'})
        self.assertEqual(response.status_code, 200, msg=f'Project must be updated {response.json()}')
        project.refresh_from_db()
        self.assertEqual(project.description, 'test2',
                         msg=f'Project description must be correct: {project.description}')

    def test_delete_project(self):
        prev_count = Project.objects.count()
        c.post(self.api_url, {'title': 'test', 'description': 'test'})
        project = Project.objects.get(title='test')
        response = c.delete(S_URL + reverse("todo:projects-detail", kwargs={'pk': project.id}))
        self.assertEqual(response.status_code, 204, msg=f'Project must be deleted {response.status_code}')
        self.assertEqual(Project.objects.count(), prev_count, msg=f'Project must be deleted {response.status_code}')

    def test_put_project(self):
        c.post(self.api_url, {'title': 'test', 'description': 'test'})
        project = Project.objects.get(title='test')
        response = c.put(S_URL + reverse("todo:projects-detail", kwargs={'pk': project.id}),
                         json={'title': 'test2', 'description': 'test2'})
        self.assertEqual(response.status_code, 405, msg=f'Project must not be updated {response.json()}')


class TagTestCase(TestCase):
    def setUp(self) -> None:
        self.api_url = S_URL + reverse("todo:tags-list")

    def test_create_tag(self):
        response = c.post(self.api_url, {'title': 'test'})
        self.assertEqual(response.status_code, 201, msg=f'Tag must be created {response.json()}')
        tag = Tag.objects.get(title='test')
        self.assertEqual(tag.title, 'test', msg=f'Tag title must be correct: {tag.title}')

    def test_update_tag(self):
        c.post(self.api_url, {'title': 'test'})
        tag = Tag.objects.get(title='test')
        response = c.patch(S_URL + reverse("todo:tags-detail", kwargs={'pk': tag.id}),
                           json={'title': 'test2'})
        self.assertEqual(response.status_code, 200, msg=f'Tag must be updated {response.json()}')
        tag.refresh_from_db()
        self.assertEqual(tag.title, 'test2', msg=f'Tag title must be correct: {tag.title}')

    def test_delete_tag(self):
        prev_count = Tag.objects.count()
        c.post(self.api_url, {'title': 'test'})
        tag = Tag.objects.get(title='test')
        response = c.delete(S_URL + reverse("todo:tags-detail", kwargs={'pk': tag.id}))
        self.assertEqual(response.status_code, 204, msg=f'Tag must be deleted {response.status_code}')
        self.assertEqual(Tag.objects.count(), prev_count, msg=f'Tag must be deleted {response.status_code}')

    def test_put_tag(self):
        c.post(self.api_url, {'title': 'test'})
        tag = Tag.objects.get(title='test')
        response = c.put(S_URL + reverse("todo:tags-detail", kwargs={'pk': tag.id}),
                         json={'title': 'test2'})
        self.assertEqual(response.status_code, 405, msg=f'Tag must not be updated {response.json()}')

