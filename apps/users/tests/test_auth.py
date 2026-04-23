import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.users.models import Profile

User = get_user_model()

@pytest.fixture
def user_data():
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123",
        "password_confirm": "password123",
        "full_name": "Test User",
        "identification": "12345678",
        "role": "STUDENT"
    }

@pytest.mark.django_db
class TestRegistration:
    def test_registration_success(self, client, user_data):
        url = reverse('register')
        response = client.post(url, user_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.count() == 1
        assert Profile.objects.count() == 1
        assert User.objects.get().username == user_data["username"]

    def test_registration_duplicate_username(self, client, user_data):
        url = reverse('register')
        client.post(url, user_data)
        
        # Intentar registrar con el mismo username
        response = client.post(url, user_data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "username" in response.data
        # Verificamos que no se cre un segundo perfil por error
        assert User.objects.count() == 1

    def test_registration_missing_fields(self, client):
        url = reverse('register')
        response = client.post(url, {})
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        # Debe reportar errores en mltiples campos
        assert "username" in response.data
        assert "email" in response.data
        assert "password" in response.data

    def test_registration_password_mismatch(self, client, user_data):
        url = reverse('register')
        user_data["password_confirm"] = "mismatch"
        response = client.post(url, user_data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "password_confirm" in response.data

@pytest.mark.django_db
class TestLogin:
    def test_login_success_and_cookies(self, client, user_data):
        # Registrar primero
        register_url = reverse('register')
        client.post(register_url, user_data)
        
        login_url = reverse('login')
        login_payload = {
            "username": user_data["username"],
            "password": user_data["password"]
        }
        response = client.post(login_url, login_payload)
        
        assert response.status_code == status.HTTP_200_OK
        # Verificar tokens en cookies HttpOnly
        assert 'access_token' in client.cookies
        assert 'refresh_token' in client.cookies
        assert client.cookies['access_token']['httponly'] is True
        # Verificar respuesta JSON
        assert "user" in response.data
        assert response.data["user"]["username"] == user_data["username"]

    def test_login_invalid_password(self, client, user_data):
        register_url = reverse('register')
        client.post(register_url, user_data)
        
        login_url = reverse('login')
        login_payload = {
            "username": user_data["username"],
            "password": "wrongpassword"
        }
        response = client.post(login_url, login_payload)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "detail" in response.data

@pytest.mark.django_db
class TestUserProfile:
    def test_get_me_authenticated(self, client, user_data):
        # Registrar y loguear para obtener cookies
        register_url = reverse('register')
        client.post(register_url, user_data)
        
        login_url = reverse('login')
        login_payload = {
            "username": user_data["username"],
            "password": user_data["password"]
        }
        client.post(login_url, login_payload)
        
        # Probar endpoint /me
        me_url = reverse('me')
        response = client.get(me_url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["username"] == user_data["username"]
        assert response.data["role"] == "STUDENT"

    def test_get_me_unauthenticated(self, client):
        me_url = reverse('me')
        response = client.get(me_url)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
