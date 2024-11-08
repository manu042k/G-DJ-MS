from django.urls import path
from . import views
from .views import ProductViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    # path('', views.index, name='index'),
] + router.urls