from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework.test import RequestsClient

from .models import Project, Tag, Task, Change

User = get_user_model()

c = RequestsClient()

S_URL = "http://testserver"


# noinspection DuplicatedCode
class ProjectTestCase(TestCase):
    def setUp(self) -> None:
        self.api_url = S_URL + reverse("todo:projects-list")
        User.objects.create_user(username='test', password='test')
        response = c.post(S_URL + reverse("users:token_obtain_pair"), {'username': 'test', 'password': 'test'})
        self.header1 = {'Authorization': f'Bearer {response.json()["access"]}'}
        User.objects.create_user(username='test2', password='test2')
        response = c.post(S_URL + reverse("users:token_obtain_pair"), {'username': 'test2', 'password': 'test2'})
        self.header2 = {'Authorization': f'Bearer {response.json()["access"]}'}

    def test_create_project(self):
        response = c.post(self.api_url, {'title': 'test', 'description': 'test'}, headers=self.header1)
        self.assertEqual(response.status_code, 201, msg=f'Project must be created {response.json()}')
        project = Project.objects.get(title='test')
        self.assertEqual(project.description, 'test', msg=f'Project description must be correct: {project.description}')
        self.assertEqual(project.owner.username, 'test', msg=f'Project owner must be correct: {project.owner.username}')

    def test_create_project_without_auth(self):
        response = c.post(self.api_url, {'title': 'test', 'description': 'test'})
        self.assertEqual(response.status_code, 401, msg=f'Project must not be created {response.json()}')

    def test_update_project(self):
        c.post(self.api_url, {'title': 'test', 'description': 'test'}, headers=self.header1)
        project = Project.objects.get(title='test')
        response = c.patch(S_URL + reverse("todo:projects-detail", kwargs={'pk': project.id}),
                           {'description': 'test2'}, headers=self.header1)
        self.assertEqual(response.status_code, 200, msg=f'Project must be updated {response.status_code}')
        project.refresh_from_db()
        self.assertEqual(project.description, 'test2',
                         msg=f'Project description must be correct: {project.description}')
        # update with different user
        response = c.patch(S_URL + reverse("todo:projects-detail", kwargs={'pk': project.id}),
                           json={'description': 'test3'}, headers=self.header2)
        self.assertEqual(response.status_code, 404, msg=f'Project must not be updated {response.json()}')

    def test_delete_project(self):
        prev_count = Project.objects.count()
        c.post(self.api_url, {'title': 'test', 'description': 'test'}, headers=self.header1)
        project = Project.objects.get(title='test')
        # different user
        response = c.delete(S_URL + reverse("todo:projects-detail", kwargs={'pk': project.id}), headers=self.header2)
        self.assertEqual(response.status_code, 404, msg=f'Project must not be deleted {response.status_code}')
        self.assertEqual(Project.objects.count(), prev_count + 1, msg=f'Project must not be deleted')
        # correct user
        response = c.delete(S_URL + reverse("todo:projects-detail", kwargs={'pk': project.id}), headers=self.header1)
        self.assertEqual(response.status_code, 204, msg=f'Project must be deleted {response.status_code}')
        self.assertEqual(Project.objects.count(), prev_count, msg=f'Project must be deleted {response.status_code}')

    def test_put_project(self):
        c.post(self.api_url, {'title': 'test', 'description': 'test'}, headers=self.header1)
        project = Project.objects.get(title='test')
        response = c.put(S_URL + reverse("todo:projects-detail", kwargs={'pk': project.id}),
                         json={'title': 'test2', 'description': 'test2'}, headers=self.header1)
        self.assertEqual(response.status_code, 405, msg=f'Project must not be updated {response.json()}')

    def test_deadline_before_current_date(self):
        response = c.post(self.api_url, {'title': 'test', 'deadline': '2020-01-01'}, headers=self.header1)
        self.assertEqual(response.status_code, 400, msg=f'Task must not be created {response.json()}')


# noinspection DuplicatedCode
class TagTestCase(TestCase):
    def setUp(self) -> None:
        self.api_url = S_URL + reverse("todo:tags-list")
        User.objects.create_user(username='test', password='test')
        response = c.post(S_URL + reverse("users:token_obtain_pair"), {'username': 'test', 'password': 'test'})
        self.header1 = {'Authorization': f'Bearer {response.json()["access"]}'}
        User.objects.create_user(username='test2', password='test2')
        response = c.post(S_URL + reverse("users:token_obtain_pair"), {'username': 'test2', 'password': 'test2'})
        self.header2 = {'Authorization': f'Bearer {response.json()["access"]}'}

    def test_create_tag(self):
        response = c.post(self.api_url, {'title': 'test'}, headers=self.header1)
        self.assertEqual(response.status_code, 201, msg=f'Tag must be created {response.json()}')
        tag = Tag.objects.get(title='test')
        self.assertEqual(tag.title, 'test', msg=f'Tag title must be correct: {tag.title}')

    def test_create_tag_without_auth(self):
        response = c.post(self.api_url, {'title': 'test'})
        self.assertEqual(response.status_code, 401, msg=f'Tag must not be created {response.json()}')

    def test_update_tag(self):
        c.post(self.api_url, {'title': 'test'}, headers=self.header1)
        tag = Tag.objects.get(title='test')
        response = c.patch(S_URL + reverse("todo:tags-detail", kwargs={'pk': tag.id}),
                           json={'title': 'test2'}, headers=self.header1)
        self.assertEqual(response.status_code, 200, msg=f'Tag must be updated {response.json()}')
        tag.refresh_from_db()
        self.assertEqual(tag.title, 'test2', msg=f'Tag title must be correct: {tag.title}')
        # update with different user
        response = c.patch(S_URL + reverse("todo:tags-detail", kwargs={'pk': tag.id}),
                           json={'title': 'test3'}, headers=self.header2)
        self.assertEqual(response.status_code, 404, msg=f'Tag must not be updated {response.json()}')

    def test_delete_tag(self):
        prev_count = Tag.objects.count()
        c.post(self.api_url, {'title': 'test'}, headers=self.header1)
        tag = Tag.objects.get(title='test')
        response = c.delete(S_URL + reverse("todo:tags-detail", kwargs={'pk': tag.id}))
        self.assertEqual(response.status_code, 401, msg=f'Tag must not be deleted {response.json()}')
        self.assertEqual(Tag.objects.count(), prev_count + 1, msg=f'Tag must not be deleted')
        # correct user
        response = c.delete(S_URL + reverse("todo:tags-detail", kwargs={'pk': tag.id}), headers=self.header1)
        self.assertEqual(response.status_code, 204, msg=f'Tag must be deleted {response.status_code}')
        self.assertEqual(Tag.objects.count(), prev_count, msg=f'Tag must be deleted {response.status_code}')

    def test_put_tag(self):
        c.post(self.api_url, {'title': 'test'}, headers=self.header1)
        tag = Tag.objects.get(title='test')
        response = c.put(S_URL + reverse("todo:tags-detail", kwargs={'pk': tag.id}),
                         json={'title': 'test2'}, headers=self.header1)
        self.assertEqual(response.status_code, 405, msg=f'Tag must not be updated {response.json()}')


# noinspection DuplicatedCode
class TaskTestCase(TestCase):
    def setUp(self) -> None:
        self.api_url = S_URL + reverse("todo:tasks-list")
        User.objects.create_user(username='test', password='test')
        response = c.post(S_URL + reverse("users:token_obtain_pair"), {'username': 'test', 'password': 'test'})
        self.header1 = {'Authorization': f'Bearer {response.json()["access"]}'}
        User.objects.create_user(username='test2', password='test2')
        response = c.post(S_URL + reverse("users:token_obtain_pair"), {'username': 'test2', 'password': 'test2'})
        self.header2 = {'Authorization': f'Bearer {response.json()["access"]}'}

    def test_create_task(self):
        response = c.post(self.api_url, {'title': 'test', 'description': 'test'}, headers=self.header1)
        self.assertEqual(response.status_code, 201, msg=f'Task must be created {response.json()}')
        task = Task.objects.get(title='test')
        self.assertEqual(task.description, 'test', msg=f'Task description must be correct: {task.description}')

    def test_create_task_without_auth(self):
        response = c.post(self.api_url, {'title': 'test', 'description': 'test'})
        self.assertEqual(response.status_code, 401, msg=f'Task must not be created {response.json()}')

    def test_update_task(self):
        c.post(S_URL + reverse("todo:tasks-list"), {'title': 'test', 'description': 'test'}, headers=self.header1)
        task = Task.objects.get(title='test')
        response = c.patch(S_URL + reverse("todo:tasks-detail", kwargs={'pk': task.id}),
                           json={'description': 'test2'}, headers=self.header2)
        self.assertEqual(response.status_code, 404, msg=f'Task must not be updated {response.json()}')
        # correct user
        response = c.patch(S_URL + reverse("todo:tasks-detail", kwargs={'pk': task.id}),
                           json={'description': 'test2'}, headers=self.header1)
        self.assertEqual(response.status_code, 200, msg=f'Task must be updated {response.json()}')
        task.refresh_from_db()
        self.assertEqual(task.description, 'test2', msg=f'Task description must be correct: {task.description}')

    def test_delete_task(self):
        prev_count = Task.objects.count()
        c.post(S_URL + reverse("todo:tasks-list"), {'title': 'test', 'description': 'test'}, headers=self.header1)
        task = Task.objects.get(title='test')
        response = c.delete(S_URL + reverse("todo:tasks-detail", kwargs={'pk': task.id}), headers=self.header2)
        self.assertEqual(response.status_code, 404, msg=f'Task must not be deleted {response.json()}')
        self.assertEqual(Task.objects.count(), prev_count + 1, msg=f'Task must not be deleted')
        # correct user
        response = c.delete(S_URL + reverse("todo:tasks-detail", kwargs={'pk': task.id}), headers=self.header1)
        self.assertEqual(response.status_code, 204, msg=f'Task must be deleted {response.status_code}')
        self.assertEqual(Task.objects.count(), prev_count, msg=f'Task must be deleted {response.status_code}')

    def test_put_task(self):
        c.post(S_URL + reverse("todo:tasks-list"), {'title': 'test', 'description': 'test'}, headers=self.header1)
        task = Task.objects.get(title='test')
        response = c.put(S_URL + reverse("todo:tasks-detail", kwargs={'pk': task.id}),
                         json={'title': 'test2', 'description': 'test2'}, headers=self.header1)
        self.assertEqual(response.status_code, 405, msg=f'Task must not be updated {response.json()}')

    def test_deadline_before_current_date(self):
        response = c.post(self.api_url, {'title': 'test', 'deadline': '2020-01-01'}, headers=self.header1)
        self.assertEqual(response.status_code, 400, msg=f'Task must not be created {response.json()}')

    def test_priority(self):
        response = c.post(self.api_url, {'title': 'test', 'priority': 6}, headers=self.header1)
        self.assertEqual(response.status_code, 400, msg=f'Task must not be created {response.json()}')
        response = c.post(self.api_url, {'title': 'test', 'priority': -1}, headers=self.header1)
        self.assertEqual(response.status_code, 400, msg=f'Task must not be created {response.json()}')


# noinspection DuplicatedCode
class ChangeTestCase(TestCase):
    def setUp(self) -> None:
        self.api_url = S_URL + reverse("todo:changes-list")
        User.objects.create_user(username='test', password='test')
        response = c.post(S_URL + reverse("users:token_obtain_pair"), {'username': 'test', 'password': 'test'})
        self.header1 = {'Authorization': f'Bearer {response.json()["access"]}'}
        User.objects.create_user(username='test2', password='test2')
        response = c.post(S_URL + reverse("users:token_obtain_pair"), {'username': 'test2', 'password': 'test2'})
        self.header2 = {'Authorization': f'Bearer {response.json()["access"]}'}

    def test_create_change(self):
        response = c.post(self.api_url, {'action': Change.CREATED}, headers=self.header1)
        self.assertEqual(response.status_code, 405, msg=f'Change can not be created {response.json()}')

    def test_update_change(self):
        response = c.patch(self.api_url, {'action': Change.UPDATED}, headers=self.header1)
        self.assertEqual(response.status_code, 405, msg=f'Change can not be updated {response.json()}')

    def test_delete_change(self):
        response = c.delete(self.api_url, headers=self.header1)
        self.assertEqual(response.status_code, 405, msg=f'Change can not be deleted {response.json()}')

    def test_get_change(self):
        Change.objects.create(action=Change.CREATED, owner=User.objects.get(username='test'),
                              content_type=Change.PROJECT, object_id=1, change_id=1)
        response = c.get(S_URL + reverse('todo:changes-detail', kwargs={'change_id': 1}), headers=self.header1)
        self.assertEqual(response.status_code, 200, msg=f'Change must be received {response.json()}')
        response = c.get(S_URL + reverse('todo:changes-detail', kwargs={'change_id': 1}), headers=self.header2)
        self.assertEqual(response.status_code, 404, msg=f'Change must not be received {response.json()}')
        response = c.get(S_URL + reverse('todo:changes-detail', kwargs={'change_id': 2}), headers=self.header1)
        self.assertEqual(response.status_code, 404, msg=f'Change must not be received {response.json()}')
