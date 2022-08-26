
from cgitb import lookup
from sys import call_tracing
from django.urls import path,include
from . import views
#from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
#router=DefaultRouter()

router=routers.DefaultRouter()
router.register('products',views.ProductViewSet,basename='products')
router.register('collections',views.CollectionViewSet)
router.register('carts',views.CartViewSet)
router.register('customers',views.CustomerViewSet)
cart_router=routers.NestedDefaultRouter(router,'carts',lookup='cart')
cart_router.register('items',views.CartItemViewSet,basename='cart-item')
product_router=routers.NestedDefaultRouter(router,'products',lookup='product')
product_router.register('reviews',views.ReviewsViewSet,basename='product-reviews')
urlpatterns=router.urls+product_router.urls+cart_router.urls
  
# i can use this shape if there are extra urls 
# urlpatterns = [
#     path("",include(router.urls)),

# ]
