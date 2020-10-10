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
    path('customer',views.customer,name='customer'),
    path("customerdel/<int:id>/",views.customerdel,name="customerdel" ),
    path('user',views.user,name='user'),
    path('user/<int:id>/',views.userBlock,name='userblock'),
    path('userdelete/<int:id>/',views.userDelete,name='userdelete'),
    path('userupdate/<int:id>/',views.userUpdate,name='userupdate'),
    path('checking/<int:id>/<str:value>/',views.checking,name='checking'),
    
]
