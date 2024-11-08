# import logging
# from django.core.cache import cache
# from rest_framework.response import Response
# from rest_framework import viewsets
# from .models import Product
# from .serializers import ProductSerializer
# from rest_framework.permissions import IsAuthenticated

# class ProductModelViewSet(viewsets.ModelViewSet):
#     permission_classes = [IsAuthenticated]
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

#     def list(self, request, *args, **kwargs):
#         # Check cache first, else return the response
#         product_list = cache.get('product_list')
#         if not product_list:
#             response = super().list(request, *args, **kwargs)
#             product_list = response.data  # Serialize data
#             cache.set('product_list', product_list, 60 * 15)  # Cache for 15 minutes
#             print('Cache miss')
#         return Response(product_list)

#     def retrieve(self, request, *args, **kwargs):
#         product = cache.get(f'product_{kwargs["pk"]}')
#         if not product:
#             response = super().retrieve(request, *args, **kwargs)
#             product = response.data  # This is the actual data, not the response object
#             cache.set(f'product_{kwargs["pk"]}', product, 60 * 15)
#         return Response(product)

#     def create(self, request, *args, **kwargs):
#         response = super().create(request, *args, **kwargs)
#         cache.delete('product_list')  # Invalidate list cache
#         print('Cache invalidated')
#         return response

#     def update(self, request, *args, **kwargs):
#         response = super().update(request, *args, **kwargs)
#         cache.delete(f'product_{kwargs["pk"]}')  # Invalidate specific product cache
#         cache.delete('product_list')  # Invalidate list cache
#         return response

#     def destroy(self, request, *args, **kwargs):
#         response = super().destroy(request, *args, **kwargs)
#         cache.delete(f'product_{kwargs["pk"]}')  # Invalidate specific product cache
#         cache.delete('product_list')  # Invalidate list cache
#         return response


from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @method_decorator(cache_page(60 * 60 * 2))  # Cache for 2 hours
    @method_decorator(vary_on_cookie)  # Vary on cookie if needed for user-specific caching
    def list(self, request):
        """
        List all products and cache the response for 2 hours.
        """
        queryset = Product.objects.all()
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)

    @method_decorator(cache_page(60 * 60 * 2))  # Cache for 2 hours
    @method_decorator(vary_on_headers("Authorization"))  # Vary based on Authorization header
    def retrieve(self, request, pk=None):
        """
        Retrieve a single product and cache the response for 2 hours.
        """
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def create(self, request):
        """
        Create a new product.
        Cache for the product list will be deleted after creation.
        """
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete('product_list')  # Clear product list cache
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def update(self, request, pk=None):
        """
        Update an existing product.
        Cache for the product and list will be deleted.
        """
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            cache.delete(f'product_{pk}')  # Clear cached product
            cache.delete('product_list')  # Clear product list cache
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        """
        Delete a product.
        Cache for the product and list will be deleted.
        """
        product = Product.objects.get(pk=pk)
        product.delete()
        cache.delete(f'product_{pk}')  # Clear cached product
        cache.delete('product_list')  # Clear product list cache
        return Response(status=204)
