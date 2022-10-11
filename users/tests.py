from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework.test import RequestsClient

User = get_user_model()

c = RequestsClient()

S_URL = "http://testserver"


class UserTestCase(TestCase):
    def setUp(self) -> None:
        self.api_url = S_URL + reverse("users:users-list")

    def test_create_user(self):
        response = c.post(self.api_url, {'username': 'test', 'password': 'test', 'is_active': True})
        self.assertEqual(response.status_code, 201, msg=f'User must be created {response.json()}')
        user = User.objects.get(username='test')
        self.assertEqual(user.is_active, True, msg=f'User must be active {user.is_active}')
        assert (user.check_password('test'), 'Password must be correct')

    def test_get_token(self):
        c.post(self.api_url, {'username': 'test', 'password': 'test', 'is_active': True})
        response = c.post(S_URL + reverse("users:token_obtain_pair"), {'username': 'test', 'password': 'test'})
        self.assertEqual(response.status_code, 200, msg=f'Token must be created {response.json()}')
        access = response.json()['access']
        refresh = response.json()['refresh']
        response = c.post(S_URL + reverse("users:token_refresh"), {'refresh': refresh})
        self.assertEqual(response.status_code, 200, msg=f'Token must be refreshed {response.json()}')
        response = c.post(S_URL + reverse("users:token_verify"), {'token': access})
        self.assertEqual(response.status_code, 200, msg=f'Token must be verified {response.json()}')

    def test_update_user_active(self):
        c.post(self.api_url, {'username': 'test', 'password': 'test', 'is_active': True})
        response = c.post(S_URL + reverse("users:token_obtain_pair"), {'username': 'test', 'password': 'test'})
        access = response.json()['access']
        user = User.objects.get(username='test')
        response = c.patch(S_URL + reverse("users:users-detail", kwargs={'pk': user.id}),
                           json={'is_active': False}, headers={'Authorization': f'Bearer {access}'})
        self.assertEqual(response.status_code, 200, msg=f'User must be updated {response.json()}')
        user.refresh_from_db()
        self.assertFalse(user.is_active, msg=f'User must be inactive {user.is_active}')
        user.is_active = True
        user.save()
