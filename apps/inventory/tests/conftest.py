import pytest
from rest_framework.test import APIClient
from apps.users.models import User

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(
        username='admin_test', 
        email='admin_test@test.com', 
        password='password123'
    )

@pytest.fixture
def api_admin_client(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    return api_client
