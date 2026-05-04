import pytest
import base64
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from apps.payments.models import Currency, PaymentMethod, PaymentType

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

    @pytest.fixture
    def payment_catalogs(self):
        currency, _ = Currency.objects.get_or_create(
            code="USD",
            defaults={"name": "Dólares", "symbol": "$"},
        )
        payment_type, _ = PaymentType.objects.get_or_create(name="Transferencia")
        alternate_type, _ = PaymentType.objects.get_or_create(name="Efectivo")
        return {
            "currency": currency,
            "payment_type": payment_type,
            "alternate_type": alternate_type,
        }

    def test_create_payment_method_success(self, admin_client, payment_catalogs):
        url = reverse('paymentmethod-list')
        image = SimpleUploadedFile(
            "metodo.png",
            base64.b64decode(
                "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVR4nGNgYGAAAAAEAAH2FzhVAAAAAElFTkSuQmCC"
            ),
            content_type="image/png",
        )
        data = {
            "name": "Pago Móvil",
            "payment_type": payment_catalogs["payment_type"].id,
            "currency": payment_catalogs["currency"].id,
            "details": "0412-1234567, Banesco",
            "image": image,
        }
        response = admin_client.post(url, data, format="multipart")
        assert response.status_code == status.HTTP_201_CREATED
        assert PaymentMethod.objects.count() == 1
        created_method = PaymentMethod.objects.first()
        assert created_method.name == "Pago Móvil"
        assert "metodo" in created_method.image.name
        assert created_method.image.name.endswith(".png")

    def test_create_payment_method_invalid_data(self, admin_client, payment_catalogs):
        url = reverse('paymentmethod-list')
        data = {
            "name": "PM",
            "payment_type": payment_catalogs["payment_type"].id,
            "currency": payment_catalogs["currency"].id,
        }
        response = admin_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_list_active_payment_methods(self, authenticated_client, payment_catalogs):
        PaymentMethod.objects.create(
            name="Activo",
            payment_type=payment_catalogs["payment_type"],
            currency=payment_catalogs["currency"],
            is_active=True,
        )
        PaymentMethod.objects.create(
            name="Inactivo",
            payment_type=payment_catalogs["payment_type"],
            currency=payment_catalogs["currency"],
            is_active=False,
        )
        
        url = reverse('paymentmethod-list')
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['name'] == "Activo"

    def test_search_and_filter(self, authenticated_client, payment_catalogs):
        PaymentMethod.objects.create(
            name="Banesco",
            payment_type=payment_catalogs["payment_type"],
            currency=payment_catalogs["currency"],
        )
        PaymentMethod.objects.create(
            name="Caja",
            payment_type=payment_catalogs["alternate_type"],
            currency=payment_catalogs["currency"],
        )
        
        url = reverse('paymentmethod-list')
        
        # Test Search
        response = authenticated_client.get(f"{url}?search=Banesco")
        assert len(response.data) == 1
        assert response.data[0]['name'] == "Banesco"
        
        # Test Filter
        response = authenticated_client.get(f"{url}?payment_type={payment_catalogs['payment_type'].id}")
        assert len(response.data) == 1
        assert response.data[0]['payment_type'] == payment_catalogs['payment_type'].id

    def test_soft_delete(self, admin_client, payment_catalogs):
        method = PaymentMethod.objects.create(
            name="Borrar",
            payment_type=payment_catalogs["payment_type"],
            currency=payment_catalogs["currency"],
        )
        url = reverse('paymentmethod-detail', kwargs={'pk': method.pk})
        
        response = admin_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        method.refresh_from_db()
        assert method.is_active is False

    def test_create_payment_method_forbidden_for_non_admin(self, authenticated_client, payment_catalogs):
        url = reverse('paymentmethod-list')
        data = {
            "name": "Hack",
            "payment_type": payment_catalogs["payment_type"].id,
            "currency": payment_catalogs["currency"].id,
        }
        
        response = authenticated_client.post(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_retrieve_non_existent_payment_method(self, authenticated_client):
        url = reverse('paymentmethod-detail', kwargs={'pk': 9999})
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_payment_method_name_too_short(self, admin_client, payment_catalogs):
        method = PaymentMethod.objects.create(
            name="Efectivo",
            payment_type=payment_catalogs["payment_type"],
            currency=payment_catalogs["currency"],
        )
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

    def test_patch_payment_method_with_image_string(self, admin_client, payment_catalogs):
        # Crear un método con imagen primero
        method = PaymentMethod.objects.create(
            name="Original",
            payment_type=payment_catalogs["payment_type"],
            currency=payment_catalogs["currency"],
            image="payment_methods/test.png"
        )
        url = reverse('paymentmethod-detail', kwargs={'pk': method.pk})
        
        # Simular lo que hace el frontend: enviar la URL de la imagen como string en el JSON
        data = {
            "name": "Actualizado",
            "image": "/media/payment_methods/test.png"
        }
        
        response = admin_client.patch(url, data, format="json")
        
        # Si el backend no maneja strings en ImageField, esto podría fallar con 400
        assert response.status_code == status.HTTP_200_OK
        method.refresh_from_db()
        assert method.name == "Actualizado"
        assert method.image.name == "payment_methods/test.png"
