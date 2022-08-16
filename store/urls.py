
from django.urls import path
from . import views

urlpatterns = [
    path('products', views.product_list),
    path('detail/<int:id>', views.product_detail),
    path('collection/<int:pk>', views.collect_detail,name='collection_detail'#used in the view name at hyperlinkrelatedfield
    ),
     path('collections', views.collection_list),
    
]
