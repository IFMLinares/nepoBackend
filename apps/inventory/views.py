from rest_framework import viewsets, permissions
from rest_framework.parsers import MultiPartParser, JSONParser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter

from .models import Category, Product, UnitOfMeasure
from .serializers import CategorySerializer, ProductSerializer, UnitOfMeasureSerializer
from .selectors import category_list, product_list, unit_of_measure_list
from .services import (
    category_create, category_update, category_delete,
    product_create, product_update, product_delete
)
from apps.users.permissions import IsAdmin

class CategoryViewSet(viewsets.ModelViewSet):
    """Gestión de categorías de inventario"""
    serializer_class = CategorySerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [IsAdmin()]

    def get_queryset(self):
        return category_list()

    def perform_create(self, serializer):
        serializer.instance = category_create(**serializer.validated_data)

    def perform_update(self, serializer):
        serializer.instance = category_update(category=self.get_object(), data=serializer.validated_data)

    def perform_destroy(self, instance):
        category_delete(category=instance)

class UnitOfMeasureViewSet(viewsets.ReadOnlyModelViewSet):
    """Listado de unidades de medida"""
    serializer_class = UnitOfMeasureSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = unit_of_measure_list()

@extend_schema_view(
    list=extend_schema(
        summary="Listar productos",
        parameters=[
            OpenApiParameter(name='categories__id', description='Filtrar por ID de categoría', required=False, type=int),
            OpenApiParameter(name='categories__name', description='Filtrar por nombre de categoría', required=False, type=str),
        ]
    ),
    create=extend_schema(summary="Crear producto", description="Soporta subida de imagen (multipart/form-data)"),
)
class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    parser_classes = [MultiPartParser, JSONParser]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name']
    filterset_fields = ['categories__id', 'categories__name']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [IsAdmin()]

    def get_queryset(self):
        return product_list()

    def perform_create(self, serializer):
        serializer.instance = product_create(**serializer.validated_data)

    def perform_update(self, serializer):
        serializer.instance = product_update(product=self.get_object(), data=serializer.validated_data)

    def perform_destroy(self, instance):
        product_delete(product=instance)
