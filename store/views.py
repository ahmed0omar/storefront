from distutils.log import error
from django.shortcuts import get_object_or_404
from .models import Product,Collection,OrderItem,Review
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import CollectionSerializer, ProductSerializer, ReviwsSerializer
from .filters import ProductsFilter

# Create your views here.
class ProductViewSet(ModelViewSet):
    queryset=Product.objects.all()
    serializer_class= ProductSerializer
    filter_backends=[DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_class=ProductsFilter
    search_fields=['title','description']
    ordering_fields=['id','title']
    pagination_class=PageNumberPagination
    #now we will use costomize filters 
    #filterset_fields=['collection_id','unit_price']
    #to apply filtering we need to override get_queryset method 
    #we didn't need this filter because we use generic filter using django-filters library
    # def get_queryset(self):
    #     queryset=Product.objects.all()
    #     collection_id=self.request.query_params.get('collection_id')
    #     if collection_id:
    #         queryset=Product.objects.filter(collection_id=collection_id)
    #     return queryset
    def get_serializer_context(self):
        return {'request': self.request}
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count()>0:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs) 

class CollectionViewSet(ModelViewSet):

    queryset=Collection.objects.all()
    serializer_class= CollectionSerializer
    pagination_class=PageNumberPagination
    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection=kwargs['pk']).count()>0:
             return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        return super().destroy(request, *args, **kwargs) 
class ReviewsViewSet(ModelViewSet):
    
    serializer_class= ReviwsSerializer
    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])
    def get_serializer_context(self):
        return {'product_id':self.kwargs['product_pk']}
    
    

    
    
   
        

    
    
   
    
