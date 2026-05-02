from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaymentMethodViewSet, CurrencyViewSet, PaymentTypeViewSet

router = DefaultRouter()
router.register(r'payment-methods', PaymentMethodViewSet, basename='paymentmethod')
router.register(r'currencies', CurrencyViewSet, basename='currency')
router.register(r'payment-types', PaymentTypeViewSet, basename='paymenttype')

urlpatterns = [
    path('', include(router.urls)),
]
