from django.urls import path
from . import views

urlpatterns=[
    path('cart-detail/',views.cart_detail,name='cart_detail'),
    path('update_item/',views.updateItem,name='update_item'),
    path('proces/',views.processOrder,name="processOrder")
    # path('add/<int:id>/', views.cart_add, name='cart_add'),
    # path('adding/<int:id>/', views.cart_adding, name='cart_adding'),
    # path('item_clear/<int:id>/', views.item_clear, name='item_clear'),
    # path('cart/item_increment/<int:id>/',views.item_increment, name='item_increment'),
    # path('cart/item_decrement/<int:id>/',views.item_decrement, name='item_decrement'),
    # path('cart_clear/', views.cart_clear, name='cart_clear'),

]