from distutils.log import error
from urllib import response
from xmlrpc.client import ResponseError
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import Product,Collection
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView,ListCreateAPIView
from .serializers import CollectionSerializer, ProductSerializer

# Create your views here.
class ProductList(ListCreateAPIView):
    queryset=Product.objects.select_related('collection').all()
    serializer_class= ProductSerializer
    def get_serializer_context(self):
        return {'request': self.request}
    
class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset=products=Product.objects.all()
    serializer_class= ProductSerializer
    lookup_field='id'
    def delete(self, request, id):
        product=get_object_or_404(Product,pk=id)
        if product.orderitems.count()> 0:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
   
        
class CollectionList(ListCreateAPIView):
    queryset=Collection.objects.all()
    serializer_class= CollectionSerializer
          
class CollectionDetail(RetrieveUpdateDestroyAPIView):
    queryset=products=Collection.objects.all()
    serializer_class= CollectionSerializer
    
    def delete(self, request, pk):
        collection=get_object_or_404(Collection,pk=pk)
        if collection.products.count()> 0:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
   
    
