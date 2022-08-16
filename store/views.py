from distutils.log import error
from urllib import response
from xmlrpc.client import ResponseError
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import Product,Collection
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CollectionSerializer, ProductSerializer

# Create your views here.
@api_view(['GET','POST'])
def product_list(request):
    if request.method =='GET':
        products=Product.objects.select_related('collection').all().order_by('id')
        serializer=ProductSerializer(
            products,many=True, context={'request': request})
        return Response(serializer.data)   
    elif request.method =='POST':
        serializer=ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
           # serializer.validated_data
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def product_detail(request,id):
   # try:
    product=get_object_or_404(Product,pk=id)
    if request.method =='GET':
        serializer=ProductSerializer(product,context={'request': request})
        return Response(serializer.data)
    elif request.method =='PUT':
        serializer=ProductSerializer(product,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)
        
    elif request.method =='DELETE':
        if product.orderitems.count()> 0:
            return Response(stuts=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        product.delete()
        return Response(stuts=status.HTTP_204_NO_CONTENT)

    #except Product.DoesNotExist:
        #return Response(status=404)
        #return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET','PUT','DELETE'])
def collect_detail(request,pk):
    collection=get_object_or_404(Collection,pk=pk)
    if request.method =='GET':
        serializer=CollectionSerializer(collection)
        return Response(serializer.data)
    elif request.method =='PUT':
        serializer=CollectionSerializer(collection,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)
        
    elif request.method =='DELETE':   
        if collection.products.count()> 0:
            return Response(stuts=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
@api_view(['GET','POST'])
def collection_list(request):
    if request.method =='GET':
        collection=Collection.objects.all()
        serializer=CollectionSerializer(collection,many=True)
        return Response(serializer.data)   
    elif request.method =='POST':
        serializer=CollectionSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
           # serializer.validated_data
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)