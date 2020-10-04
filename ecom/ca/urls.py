from django.urls import path
from . import views

urlpatterns=[
    path('cart-detail/',views.cart_detail,name='cart_detail'),
    path('update_item/',views.updateItem,name='update_item'),
    path('proces/',views.processOrder,name="processOrder")
   

]