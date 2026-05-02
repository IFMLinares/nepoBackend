from rest_framework import serializers
from .models import Category, Product, UnitOfMeasure

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class UnitOfMeasureSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitOfMeasure
        fields = ['id', 'name', 'abbreviation', 'is_active']

class ProductSerializer(serializers.ModelSerializer):
    # Para escritura: acepta IDs
    categories = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Category.objects.all(),
        required=False
    )
    unit_of_measure_details = UnitOfMeasureSerializer(source='unit_of_measure', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'quantity', 'description', 'image', 
            'unit_of_measure', 'unit_of_measure_details',
            'categories', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def to_representation(self, instance):
        """Sobrescribe la respuesta para devolver las categorías anidadas (Enfoque A)"""
        representation = super().to_representation(instance)
        # Transformamos la lista de IDs en objetos serializados
        representation['categories'] = CategorySerializer(instance.categories.all(), many=True).data
        return representation
