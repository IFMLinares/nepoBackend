from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet, UnitOfMeasureViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'units-of-measure', UnitOfMeasureViewSet, basename='unit-of-measure')

urlpatterns = [
    path('', include(router.urls)),
]
