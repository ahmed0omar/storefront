from dataclasses import fields
from decimal import Decimal
from .models import Collection,Product
from unicodedata import decimal
from rest_framework import serializers
class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Collection
        fields=['id','title']
    
class ProductSerializer(serializers.ModelSerializer):
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