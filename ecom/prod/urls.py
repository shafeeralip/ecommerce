from django.urls import path
from . import views

urlpatterns=[
    path("",views.home,name='home'),
    path("userlogin",views.userlogin,name='userlogin'),
    path('register',views.register,name='register'),
    path('userlogout',views.userlogout,name='userlogout'),
    path('prodv/<int:id>/',views.view,name='prodview'),
    path("checkout",views.checkout,name='checkout'),
    path("mobail",views.mobail,name='mobail'),
    path("otp",views.otp,name='otp'),
    path("orders",views.orders,name='orderss'),
    path("shirt",views.shirt,name='shirt'),
    path("pant",views.pant,name='pant'),
    path("shoe",views.shoe,name='shoe'),
    path("watch",views.watch,name='watch'),
    path("about",views.about,name='about'),


    
    


]