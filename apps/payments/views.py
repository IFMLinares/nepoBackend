from rest_framework import viewsets, permissions
from rest_framework.parsers import MultiPartParser, JSONParser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter

from .models import PaymentMethod, Currency, PaymentType
from .serializers import PaymentMethodSerializer, CurrencySerializer, PaymentTypeSerializer
from .selectors import payment_method_list, currency_list, payment_type_list
from .services import payment_method_create, payment_method_update, payment_method_delete
from apps.users.permissions import IsAdmin

class CurrencyViewSet(viewsets.ReadOnlyModelViewSet):
    """Listado de monedas disponibles"""
    serializer_class = CurrencySerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = currency_list()

class PaymentTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """Listado de tipos de pago disponibles"""
    serializer_class = PaymentTypeSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = payment_type_list()

@extend_schema_view(
    list=extend_schema(
        tags=['Payments Extra config'],
        summary="Listar métodos de pago",
        parameters=[
            OpenApiParameter(name='payment_type', description='ID del tipo de pago', required=False, type=int),
            OpenApiParameter(name='currency', description='ID de la moneda', required=False, type=int),
            OpenApiParameter(name='search', description='Buscar por nombre', required=False, type=str),
        ]
    ),
    create=extend_schema(tags=['Payments'], summary="Crear método de pago"),
    retrieve=extend_schema(tags=['Payments'], summary="Obtener detalle de método"),
    update=extend_schema(tags=['Payments'], summary="Actualizar método"),
    partial_update=extend_schema(tags=['Payments'], summary="Actualizar parcialmente método"),
    destroy=extend_schema(tags=['Payments'], summary="Eliminar método (Soft Delete)"),
)
class PaymentMethodViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentMethodSerializer
    parser_classes = [MultiPartParser, JSONParser]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['payment_type', 'currency']
    search_fields = ['name']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsAdmin]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return payment_method_list()

    def perform_create(self, serializer):
        serializer.instance = payment_method_create(**serializer.validated_data)

    def perform_update(self, serializer):
        serializer.instance = payment_method_update(payment_method=self.get_object(), data=serializer.validated_data)

    def perform_destroy(self, instance):
        payment_method_delete(payment_method=instance)
