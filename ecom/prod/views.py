from django.shortcuts import render,redirect
from . models import *
from django.contrib.auth.models import auth,User
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ca.utils import cookieCart,cartData
from django.contrib.auth import authenticate, login,logout
# Create your views here.

def home(request):
    if request.user.is_authenticated:
        user=request.user
        name=request.user.username
        email=request.user.email
        customer,created =Customer.objects.get_or_create(user=user,name=name,email=email)
        order,created =Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
    
    product= Product.objects.filter(product_type='shirt')
    tshirt= Product.objects.filter(product_type='t-shirt')
    pant= Product.objects.filter(product_type='pant')
    glass= Product.objects.filter(product_type='sunglass')
 
    return render(request,'index.html',{'product': product,'tshirt':tshirt,'pant':pant,'glass':glass,'cartItems':cartItems})

def userlogin(request):

    if request.method =='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        if user:
            login(request,user)
            return redirect(home)
        else:
            dicti={'error':"inavlid credention"}
            return render(request,'login.html',dicti)
    else:
        return render(request,'login.html')








    # if request.COOKIES.get('user'):
    #     return redirect(home)
    # elif request.method=='POST':
    #     username=request.POST['username']
    #     password=request.POST['password']
    #     user=auth.authenticate(username=username,password=password)
    #     if user is not None:
    #         response=redirect(home)
    #         response.set_cookie('user','user')
    #         return response
            
    #     else:
    #         dicti={'error':"inavlid credention"}

    #         return render(request,'login.html',dicti)

    # return render(request,'login.html')

    
def register(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        dicti = {"username":username,"email":email}
        if User.objects.filter(username=username).exists():
            messages.info(request,'username already taken')
            return render(request, "login.html", dicti)
        elif User.objects.filter(email=email).exists():
            messages.info(request,'email already taken')
            return render(request, "login.html", dicti)

        else:
            user=User.objects.create_user(username=username,email=email,password=password)
            user.save()
            return redirect(userlogin)
    return render(request,'login.html')


def userlogout(request):
    logout(request)
    return redirect(home)

    # response =redirect(home)
    # response.delete_cookie('user')
    # return response
    

def view(request,id):
    data = cartData(request)

    cartItems=data['cartItems']
    order=data['order']
    items=data['items']
    product=Product.objects.get(id=id)

    return render(request,'productview.html',{'product':product,'cartItems':cartItems})


def checkout(request):
    data = cartData(request)
    cartItems=data['cartItems']
    order=data['order']
    items=data['items']
     
    context = {'items':items,'order':order,'cartItems':cartItems}
    return render(request,'checkout.html',context)