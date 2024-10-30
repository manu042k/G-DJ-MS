from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('api/products', views.ProductModelViewSet, )

urlpatterns = [
    # path('', views.index, name='index'),
] + router.urls