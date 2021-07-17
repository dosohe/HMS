import pytest
from django.contrib.auth import models
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


@pytest.fixture
def user():
    return models.User.objects.create_superuser(username='test',
                                                email='test@test',
                                                password='test',
                                                first_name='test',
                                                last_name='test',
                                                )

@pytest.fixture
def client(user):
    client = APIClient()
    user.set_password('test')
    user.save()
    client.login(username='test', password='test')
    return client
