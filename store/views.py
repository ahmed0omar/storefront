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
    def get_queryset(self):
        products=Product.objects.select_related('collection').all()
        return  products
    def get_serializer(self, *args, **kwargs):
        return ProductSerializer
    def get_serializer_context(self):
        return {'request': self.request}
    

class ProductDetail(APIView):
    def get(self,request,id):
        product=get_object_or_404(Product,pk=id)
        serializer=ProductSerializer(product,context={'request': request})
        return Response(serializer.data)
    def put(self,request,id):
        product=get_object_or_404(Product,pk=id)
        serializer=ProductSerializer(product,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)
    def delete(self,request,id):
        product=get_object_or_404(Product,pk=id)
        if product.orderitems.count()> 0:
            return Response(stuts=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(stuts=status.HTTP_204_NO_CONTENT)
class CollectionList(APIView):
    def get(self,request):
        collection=Collection.objects.all()
        serializer=CollectionSerializer(collection,many=True)
        return Response(serializer.data)   
    def post(self,request):
        serializer=CollectionSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
           # serializer.validated_data
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)        
class CollectionDetail(APIView):
    def get(self,request,pk):
        collection=get_object_or_404(Collection,pk=pk)
        serializer=CollectionSerializer(collection)
        return Response(serializer.data)
    def put(self,request,pk):
        collection=get_object_or_404(Collection,pk=pk)
        serializer=CollectionSerializer(collection,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)
    def delete(self,request,pk):
        collection=get_object_or_404(Collection,pk=pk)
        if collection.products.count()> 0:
            return Response(stuts=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
