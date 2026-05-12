from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import Plan, Requirement
from .serializers import PlanSerializer, RequirementSerializer

@extend_schema_view(
    list=extend_schema(summary="Listar todos los planes", description="Obtiene un listado paginado de todos los planes con sus características."),
    retrieve=extend_schema(summary="Obtener un plan", description="Obtiene los detalles de un plan específico."),
    create=extend_schema(summary="Crear un plan", description="Crea un nuevo plan junto con sus características asociadas (anidadas)."),
    update=extend_schema(summary="Actualizar un plan", description="Actualiza un plan y reemplaza todas sus características asociadas."),
    partial_update=extend_schema(summary="Actualización parcial de un plan", description="Actualiza parcialmente los campos de un plan."),
    destroy=extend_schema(summary="Eliminar un plan", description="Elimina un plan y, en cascada, sus características.")
)
class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.prefetch_related('features').all()
    serializer_class = PlanSerializer
    # Por defecto usará IsAuthenticated global

    @extend_schema(
        summary="Planes Activos para Landing",
        description="Devuelve todos los planes activos (is_active=True) para mostrar en la landing page. Endpoint de acceso público.",
        responses={200: PlanSerializer(many=True)}
    )
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def active_plans(self, request):
        active_plans = self.get_queryset().filter(is_active=True)
        serializer = self.get_serializer(active_plans, many=True)
        return Response(serializer.data)

@extend_schema_view(
    list=extend_schema(summary="Listar requisitos", description="Obtiene todos los requisitos informativos."),
    create=extend_schema(summary="Crear requisito", description="Crea un nuevo bloque de requisito."),
    update=extend_schema(summary="Actualizar requisito", description="Reemplaza un bloque de requisito."),
    destroy=extend_schema(summary="Eliminar requisito", description="Elimina un requisito del sistema.")
)
class RequirementViewSet(viewsets.ModelViewSet):
    queryset = Requirement.objects.all()
    serializer_class = RequirementSerializer

    @extend_schema(
        summary="Requisitos Activos para Landing",
        description="Devuelve los requisitos activos (is_active=True). Endpoint de acceso público.",
        responses={200: RequirementSerializer(many=True)}
    )
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def active_requirements(self, request):
        active_reqs = self.get_queryset().filter(is_active=True)
        serializer = self.get_serializer(active_reqs, many=True)
        return Response(serializer.data)
