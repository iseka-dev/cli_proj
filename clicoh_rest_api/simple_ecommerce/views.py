from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import ProductSerializer, OrderSerializer

# Create your views here.

class ProductViewSet(ModelViewSet):
    """
    A simple ViewSet for viewing and editing products.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class OrderViewSet(ModelViewSet):
    """
    A simple ViewSet for viewing and editing orders.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
