from rest_framework import serializers
from .models import PaymentMethod, Currency, PaymentType

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['id', 'name', 'code', 'symbol']

class PaymentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentType
        fields = ['id', 'name']

class PaymentMethodSerializer(serializers.ModelSerializer):
    payment_type_details = PaymentTypeSerializer(source='payment_type', read_only=True)
    currency_details = CurrencySerializer(source='currency', read_only=True)

    class Meta:
        model = PaymentMethod
        fields = [
            'id', 'name', 'payment_type', 'payment_type_details',
            'currency', 'currency_details',
            'details', 'image', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def to_internal_value(self, data):
        # Si la imagen viene como string (ej. la URL que manda el frontend), la quitamos
        # para que no falle la validación del ImageField y se mantenga la imagen actual.
        if 'image' in data and isinstance(data['image'], str):
            data = data.copy()
            data.pop('image')
        return super().to_internal_value(data)

    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("El nombre debe tener al menos 3 caracteres.")
        return value
