from django.shortcuts import render,redirect
from . models import Product
from ecom.settings import MEDIA_ROOT, MEDIA_URL
from django.contrib.auth.models import auth,User
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    product= Product.objects.filter(product_type='shirt')
    tshirt= Product.objects.filter(product_type='t-shirt')
    pant= Product.objects.filter(product_type='pant')
    glass= Product.objects.filter(product_type='sunglass')
    return render(request,'index.html',{'product': product,'tshirt':tshirt,'pant':pant,'glass':glass})

# def login(request):
#     if request.method=='POST':
#         username=request.POST['username']
#         password=request.POST['password']
#         user=auth.authenticate(username=username,password=password)
#         if user is not None:
#              auth.login(request,user)
#              return redirect(home)
#         else:
#             messages.info(request,'**invalid credentions')
#             return HttpResponseRedirect(request.path_info)

#     return render(request,'login.html')

    
# def register(request):
#     if request.method=='POST':
#         username=request.POST['username']
#         email=request.POST['email']
#         password=request.POST['password']
#         dicti = {"username":username,"email":email}
#         if User.objects.filter(username=username).exists():
#             messages.info(request,'username already taken')
#             return render(request, "login.html", dicti)
#         elif User.objects.filter(email=email).exists():
#             messages.info(request,'email already taken')
#             return render(request, "login.html", dicti)

#         else:
#             user=User.objects.create_user(username=username,email=email,password=password)
#             user.save()
#             return redirect(login)
#     return render(request,'login.html')




    