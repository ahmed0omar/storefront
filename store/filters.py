from django_filters.rest_framework import FilterSet
from .models import Product
class ProductsFilter(FilterSet):
    class Meta:
        model=Product
        fields={
            'collection_id':['exact'], #collection_id=passed value in filter
            'unit_price':['gt','lt'], #unitprice >passed value and <less than another passed value
        }