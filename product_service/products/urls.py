from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'product', views.ProductModelViewSet, basename='product')

urlpatterns = [
    # path('', views.index, name='index'),
] + router.urls