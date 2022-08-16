
from django.urls import path
from . import views

urlpatterns = [
    path('products', views.ProductList.as_view()),
    path('detail/<int:id>', views.ProductDetail.as_view()),
    path('collection/<int:pk>', views.CollectionDetail.as_view(),name='collection_detail'#used in the view name at hyperlinkrelatedfield
    ),
     path('collections', views.CollectionList.as_view()),
    
]
