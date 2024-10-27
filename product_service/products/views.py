from django.shortcuts import render
from .serializers import ProductSerializer  # Add this import
from rest_framework import viewsets # type: ignore 0
from .models import Product
from .serializers import ProductSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated # type: ignore

# Create your views here.


class ProductModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer 

    def retrieve(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        print(response.data)
        return response
