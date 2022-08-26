from distutils.log import error
from pprint import pprint
from urllib import response
from django.shortcuts import get_object_or_404,render
from django.http import QueryDict
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import action
from .models import Customer, Order, Product,Collection,OrderItem,Review,Cart,CartItem
from rest_framework import status
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import CollectionSerializer, OrderSerializer,CustomerSerializer, ProductSerializer, ReviwsSerializer,CartSerializer,CartItemSerializer,AddtemSerializer,UpdatetemSerializer
from .filters import ProductsFilter
from .permissions import AdminOrReadOnly,AdminOrAuthenticated,ViewHistoryPermission

# Create your views here.
class ProductViewSet(ModelViewSet):
    queryset=Product.objects.all()
    serializer_class= ProductSerializer
    filter_backends=[DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_class=ProductsFilter
    search_fields=['title','description']
    ordering_fields=['id','title']
    pagination_class=PageNumberPagination
    permission_classes=[AdminOrReadOnly]
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
    permission_classes=[AdminOrReadOnly]
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
    
    
class CartViewSet(CreateModelMixin,
                  DestroyModelMixin,
                  ListModelMixin,
                  RetrieveModelMixin,
                  GenericViewSet):
    queryset=Cart.objects.prefetch_related('items__product').all()
    serializer_class= CartSerializer
    pagination_class=PageNumberPagination
    

class CartItemViewSet(ModelViewSet):
    http_method_names=['post','get','delete','patch'] # here to detrmine accepted request methods
    pagination_class=PageNumberPagination
    def get_serializer_class(self):
        if self.request.method=="POST":
            return AddtemSerializer
        elif self.request.method=="PUT" or self.request.method=="PATCH":
            return UpdatetemSerializer
        return CartItemSerializer
    def get_serializer_context(self):
        return {'cart_id':self.kwargs['cart_pk']}
       
    def get_queryset(self):
        return CartItem.objects\
        .select_related('product')\
        .filter(cart=self.kwargs['cart_pk'])
    
class CustomerViewSet(ModelViewSet):
    queryset=Customer.objects.all()
    serializer_class=CustomerSerializer
    permission_classes=[AdminOrAuthenticated]
    # def get_permissions(self):
    #     if self.request.method=='GET':
    #         return [permissions.AllowAny()]
    #     return [permissions.IsAuthenticated()]
    @action(detail=True,methods=['GET'],permission_classes=[ViewHistoryPermission])
    def history(self,request,pk):
        orders=Order.objects.filter(customer_id=pk)
        serilizer=OrderSerializer(orders,many=True)
        return Response(serilizer.data)



    @action(detail=False,methods=['GET','PUT'],permission_classes=[permissions.IsAuthenticated])
    def me(self,request):
        try:
            customer=Customer.objects.get(user_id= request.user.id)
            if request.method=='GET': 
                serializer=CustomerSerializer(customer)
                return Response(serializer.data)
        except ObjectDoesNotExist: 
                    return Response({'detail':f"ther is no customer with this user {request.user.username}"},status=status.HTTP_404_NOT_FOUND)



    
    
   
    
