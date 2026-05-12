import pytest
from django.db.utils import IntegrityError
from apps.plans.models import Plan, PlanFeature
from apps.plans.services import create_plan_with_features, update_plan_with_features

@pytest.mark.django_db
class TestPlanServices:
    def test_create_plan_happy_case(self):
        """Prueba que el plan y sus características se crean exitosamente."""
        plan_data = {
            "name": "Plan Pro",
            "price": "99.99",
            "is_active": True
        }
        features_data = [
            {"description": "Feature 1", "is_included": True},
            {"description": "Feature 2", "is_included": False}
        ]
        
        plan = create_plan_with_features(plan_data, features_data)
        
        # Validaciones
        assert Plan.objects.count() == 1
        assert plan.name == "Plan Pro"
        assert PlanFeature.objects.count() == 2
        assert plan.features.count() == 2

    def test_create_plan_error_rollback(self):
        """
        Prueba que si falla la creación de una característica (ej. error de integridad por falta de campo),
        no se crea el plan debido al rollback de transaction.atomic().
        """
        plan_data = {
            "name": "Plan Fallido",
            "price": "50.00"
        }
        # Para forzar un fallo y probar la atomicidad sin depender de las validaciones de SQLite,
        # enviaremos un diccionario que lance un KeyError interno, o simularemos un error.
        from unittest.mock import patch
        
        features_data = [{"description": "Feature de prueba", "is_included": True}]
        
        with patch('apps.plans.models.PlanFeature.objects.bulk_create') as mock_bulk:
            mock_bulk.side_effect = Exception("Fallo forzado en BD")
            with pytest.raises(Exception):
                create_plan_with_features(plan_data, features_data)
            
        # Validación CRÍTICA: Asegurar que el plan tampoco se guardó
        assert Plan.objects.count() == 0
        assert PlanFeature.objects.count() == 0

    def test_update_plan_happy_case(self):
        """Prueba que un plan se actualiza y reemplaza correctamente sus características."""
        plan = Plan.objects.create(name="Plan Viejo", price="10.00")
        PlanFeature.objects.create(plan=plan, description="Vieja feature")
        
        new_plan_data = {
            "name": "Plan Nuevo",
            "price": "20.00"
        }
        new_features_data = [
            {"description": "Nueva feature 1", "is_included": True},
            {"description": "Nueva feature 2", "is_included": True}
        ]
        
        updated_plan = update_plan_with_features(plan, new_plan_data, new_features_data)
        
        # Validaciones
        assert updated_plan.name == "Plan Nuevo"
        assert updated_plan.price == "20.00"
        assert updated_plan.features.count() == 2
        assert updated_plan.features.first().description == "Nueva feature 1"

@pytest.mark.django_db
class TestPlanAPI:
    def test_create_plan_api_happy_path(self, api_client):
        """Prueba la creación anidada de un plan desde la API."""
        payload = {
            "name": "Plan API",
            "price": "19.99",
            "features": [
                {"description": "Feature API", "is_included": True}
            ]
        }
        
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.create_user(username='admin', email='admin@test.com', password='pwd')
        api_client.force_authenticate(user=user)

        response = api_client.post('/api/plans/', payload, format='json')
        
        assert response.status_code == 201
        assert response.data['name'] == "Plan API"
        assert len(response.data['features']) == 1

    def test_create_plan_api_validation_error(self, api_client):
        """Prueba que si enviamos un precio inválido, la API responde con 400."""
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.create_user(username='admin2', email='admin2@test.com', password='pwd')
        api_client.force_authenticate(user=user)

        payload = {
            "name": "Plan Invalido",
            "price": "precio-no-numerico", # Inválido
            "features": []
        }
        
        response = api_client.post('/api/plans/', payload, format='json')
        
        assert response.status_code == 400
        assert 'price' in response.data
        assert Plan.objects.count() == 0
