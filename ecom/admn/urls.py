from django .urls import path
from . import views

urlpatterns=[
    path('',views.admn,name='admn'),
    path('home',views.home,name='home'),
    # path("delete/<int:id>/",views.delete,name="delete" ),
    # path("update/<int:id>/",views.update,name='update'),
    path('addproduct',views.addproduct,name='addproduct')
    
]