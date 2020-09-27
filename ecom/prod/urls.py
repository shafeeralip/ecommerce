from django.urls import path
from . import views

urlpatterns=[
    path("",views.home,name='home'),
    path("userlogin",views.userlogin,name='userlogin'),
    path('register',views.register,name='register'),
    path('userlogout',views.userlogout,name='userlogout'),
    path('prodv/<int:id>/',views.view,name='prodview'),
    path("checkout",views.checkout,name='checkout'),

    
    


]