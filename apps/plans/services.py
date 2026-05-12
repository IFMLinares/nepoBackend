from django.db import transaction
from .models import Plan, PlanFeature

def create_plan_with_features(plan_data: dict, features_data: list) -> Plan:
    """
    Crea un Plan y sus características asociadas en una transacción atómica.
    """
    with transaction.atomic():
        # Crear el plan principal
        plan = Plan.objects.create(**plan_data)
        
        # Crear las características asociadas
        feature_objects = [
            PlanFeature(plan=plan, **feature) 
            for feature in features_data
        ]
        PlanFeature.objects.bulk_create(feature_objects)
        
    return plan

def update_plan_with_features(plan_instance: Plan, plan_data: dict, features_data: list) -> Plan:
    """
    Actualiza un Plan y reemplaza sus características asociadas en una transacción atómica.
    """
    with transaction.atomic():
        # Actualizar campos del plan
        for attr, value in plan_data.items():
            setattr(plan_instance, attr, value)
        plan_instance.save()
        
        # Estrategia de reemplazo completo para características
        if features_data is not None:
            plan_instance.features.all().delete()
            feature_objects = [
                PlanFeature(plan=plan_instance, **feature) 
                for feature in features_data
            ]
            PlanFeature.objects.bulk_create(feature_objects)
            
    return plan_instance
