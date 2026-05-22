from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Importando as Views de cada App
from apps.customers.views import CustomerViewSet
from apps.sellers.views import SellerViewSet
from apps.products.views import ProductViewSet
from apps.sales.views import SaleViewSet

# O Router do DRF cria automaticamente todas as rotas de CRUD (GET, POST, PUT, DELETE)
router = DefaultRouter()
router.register(r"customers", CustomerViewSet, basename="customer")
router.register(r"sellers", SellerViewSet, basename="seller")
router.register(r"products", ProductViewSet, basename="product")
router.register(r"sales", SaleViewSet, basename="sale")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),  # Todas as rotas da API começam com /api/
]
