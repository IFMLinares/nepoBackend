from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlanViewSet, RequirementViewSet

app_name = 'plans'

router = DefaultRouter()
router.register(r'plans', PlanViewSet, basename='plan')
router.register(r'requirements', RequirementViewSet, basename='requirement')

urlpatterns = [
    path('', include(router.urls)),
]
