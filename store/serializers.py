from dataclasses import fields
from decimal import Decimal
from itertools import product
from .models import CartItem, Collection,Product, Review,Cart
from unicodedata import decimal
from rest_framework import serializers

class UpdatetemSerializer(serializers.ModelSerializer):
    class Meta:
        model=CartItem
        fields=['quantity']
class SimpleProductSerilizer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','title','unit_price']
class AddtemSerializer(serializers.ModelSerializer):
    product_id=serializers.IntegerField()
    
    def validate_product_id(self,value):
        if not Product.objects.filter(id=value).exists():# to use exists() method we must use filter() method
            raise serializers.ValidationError("we didn't have a product with id {} ".format(value))
        return value
    def save(self,  **kwargs):
        cart_id=self.context['cart_id']
        try:
            item=CartItem.objects.get(product_id=self.validated_data['product_id'])
            item.quantity+=self.validated_data['quantity']
            item.save()
            self.instance=item
        except CartItem.DoesNotExist:
            self.instance= CartItem.objects.create(cart_id=cart_id,**self.validated_data)
        finally:
            return self.instance
    class Meta:
        model=CartItem
        fields=['product_id','quantity']
class CartItemSerializer(serializers.ModelSerializer):
    product=SimpleProductSerilizer()
    qty_price=serializers.SerializerMethodField(read_only=True,method_name='quantityPrice')
    def quantityPrice(self,cart_item:CartItem):
        return cart_item.quantity*cart_item.product.unit_price
    class Meta:
        model=CartItem
        fields=['id','product','quantity','qty_price']
class CartSerializer(serializers.ModelSerializer):
    id=serializers.UUIDField(read_only=True)
    items=CartItemSerializer(many=True,read_only=True)
    total_price=serializers.SerializerMethodField(method_name='totalPrice')
    def totalPrice(self,cart:Cart):
        #query=CartItem.objects.filter(cart_id=cart.id)
        # total_price=0
        # for item in cart.items.all():
        #     total_price+=
        # return total_price
        return sum([item.product.unit_price*item.quantity for item in cart.items.all()])
    class Meta:
        model=Cart
        fields=['id','items','total_price']#'__all__'
class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Collection
        fields=['id','title']

class ReviwsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Review
        fields=['id','name','date','description']
    def create(self, validated_data):
        product_id=self.context['product_id']
        return Review.objects.create(product_id=product_id,**validated_data)
    
class ProductSerializer(serializers.ModelSerializer):
    collection=CollectionSerializer()
    class Meta:
        model=Product
        fields=['id','title','unit_price','inventory','tax','collection']
    #id=serializers.IntegerField()
    #title=serializers.CharField(max_length=255)
    # to change the name of field with another name that in the model you must refrense the field in the model
    #price=serializers.DecimalField(max_digits=6,decimal_places=2,source='unit_price')
    #create custom serializer field
    tax=serializers.SerializerMethodField(method_name='tax_calc')
    #collection=CollectionSerializer()
    #serilaizing relationship#
    #we need to add select related to use join in query,
    #instead of doing seperate query to select fom collection table
    #collection=serializers.StringRelatedField()
    # collection=serializers.HyperlinkedRelatedField(
    #     queryset=Collection.objects.all(),
    #     view_name='collection_detail' #the name in the path function 
    # )
    
    def tax_calc(self,product ):
        return product.unit_price *Decimal( 1.1)
    #create  function ovveride
    # def create(self, validated_data):
    #     product=Product(**validated_data)
    #     product.other=1
    #     product.save()
    #     return product
    #update function ovveride
    # def update(self, instance, validated_data):
    #     instance.unite_price=validated_data.get('unit_price')
    #     instance.save()
    #     return instance