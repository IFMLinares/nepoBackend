import pytest
from django.urls import reverse
from rest_framework import status
from apps.payments.models import PaymentMethod

@pytest.mark.django_db
class TestPaymentMethods:
    @pytest.fixture
    def authenticated_client(self, api_client, django_user_model):
        user = django_user_model.objects.create_user(
            username='testuser', 
            email='test@example.com', 
            password='password'
        )
        api_client.force_authenticate(user=user)
        return api_client

    @pytest.fixture
    def admin_client(self, api_client, django_user_model):
        from apps.users.models import User
        user = django_user_model.objects.create_user(
            username='adminuser', 
            email='admin@example.com', 
            password='password',
            role=User.Role.ADMIN
        )
        api_client.force_authenticate(user=user)
        return api_client

    def test_create_payment_method_success(self, admin_client):
        url = reverse('paymentmethod-list')
        data = {
            "name": "Pago Móvil",
            "method_type": "TRANSFER",
            "details": "0412-1234567, Banesco"
        }
        response = admin_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert PaymentMethod.objects.count() == 1
        assert PaymentMethod.objects.first().name == "Pago Móvil"

    def test_create_payment_method_invalid_data(self, admin_client):
        url = reverse('paymentmethod-list')
        data = {
            "name": "PM",
            "method_type": "INVALID_TYPE"
        }
        response = admin_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_list_active_payment_methods(self, authenticated_client):
        PaymentMethod.objects.create(name="Activo", method_type="CASH", is_active=True)
        PaymentMethod.objects.create(name="Inactivo", method_type="CARD", is_active=False)
        
        url = reverse('paymentmethod-list')
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['name'] == "Activo"

    def test_search_and_filter(self, authenticated_client):
        PaymentMethod.objects.create(name="Banesco", method_type="TRANSFER")
        PaymentMethod.objects.create(name="Visa", method_type="CARD")
        
        url = reverse('paymentmethod-list')
        
        # Test Search
        response = authenticated_client.get(f"{url}?search=Visa")
        assert len(response.data) == 1
        assert response.data[0]['name'] == "Visa"
        
        # Test Filter
        response = authenticated_client.get(f"{url}?method_type=TRANSFER")
        assert len(response.data) == 1
        assert response.data[0]['method_type'] == "TRANSFER"

    def test_soft_delete(self, admin_client):
        method = PaymentMethod.objects.create(name="Borrar", method_type="CASH")
        url = reverse('paymentmethod-detail', kwargs={'pk': method.pk})
        
        response = admin_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        method.refresh_from_db()
        assert method.is_active is False

    def test_create_payment_method_forbidden_for_non_admin(self, authenticated_client):
        url = reverse('paymentmethod-list')
        data = {"name": "Hack", "method_type": "CASH"}
        
        response = authenticated_client.post(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_retrieve_non_existent_payment_method(self, authenticated_client):
        url = reverse('paymentmethod-detail', kwargs={'pk': 9999})
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_payment_method_name_too_short(self, admin_client):
        method = PaymentMethod.objects.create(name="Efectivo", method_type="CASH")
        url = reverse('paymentmethod-detail', kwargs={'pk': method.pk})
        data = {"name": "Ef"} # Menos de 3 caracteres
        
        response = admin_client.patch(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "name" in response.data

    def test_list_payment_methods_unauthenticated(self, api_client):
        # Usamos api_client directo sin force_authenticate
        url = reverse('paymentmethod-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
