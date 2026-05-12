from rest_framework import serializers
from .models import Plan, PlanFeature, Requirement
from .services import create_plan_with_features, update_plan_with_features

class RequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requirement
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class PlanFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanFeature
        fields = ('id', 'description', 'is_included')
        # No se incluye 'plan' porque será inferido por el anidamiento

class PlanSerializer(serializers.ModelSerializer):
    features = PlanFeatureSerializer(many=True, required=False)

    class Meta:
        model = Plan
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def create(self, validated_data):
        features_data = validated_data.pop('features', [])
        return create_plan_with_features(validated_data, features_data)

    def update(self, instance, validated_data):
        features_data = validated_data.pop('features', None)
        return update_plan_with_features(instance, validated_data, features_data)
