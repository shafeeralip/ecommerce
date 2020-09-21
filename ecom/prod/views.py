from django.shortcuts import render
from . models import Product
from ecom.settings import MEDIA_ROOT, MEDIA_URL


# Create your views here.

def home(request):
    product=Product.objects.filter(product_type='shirt')
    tshirt=Product.objects.filter(product_type='t-shirt')
    pant=Product.objects.filter(product_type='pant')
    glass=Product.objects.filter(product_type='sunglass')
    return render(request,'index.html',{'product': product,'tshirt':tshirt,'pant':pant,'glass':glass})

   

    




    