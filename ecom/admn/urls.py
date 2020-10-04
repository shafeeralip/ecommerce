from django .urls import path
from . import views
from ecom import settings


urlpatterns=[
    path('',views.admn,name='admn'),
   
    path('productadd',views.productadd,name='productadd'),
    path('logout',views.log,name='logout'),
    path('home',views.home,name='home'),
    path("delete/<int:id>/",views.delete,name="delete" ),
    path("update/<int:id>/",views.update,name='update'),
    path('adproduct',views.adproduct,name='adproduct'),
    path('order',views.order,name='order'),
    path("approve/<int:id>/",views.approve,name='approve'),
    path('customer',views.customer,name='customer'),
    path("customerdel/<int:id>/",views.customerdel,name="customerdel" ),
    path('user',views.user,name='user'),
]
