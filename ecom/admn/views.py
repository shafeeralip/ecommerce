from django.shortcuts import render,redirect
from django.contrib import messages
from prod.models import Product
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout
from django.views.decorators.cache import cache_control


# Create your views here.

def admn(request):
  if request.user.is_authenticated:
    prod=Product.objects.all()
    return render(request,'adhome.html',{'product':prod})
  elif request.method =='POST':
    username=request.POST['username']
    password=request.POST['password']
    user=authenticate(username=username,password=password)
    if user:
        if username =='shafeerali' and password =='123':
          login(request,user)
         
          return redirect(home)
        else:
          messages.warning(request,'inavalid credention')
          return render(request,'admnlog.html')
    else:
      messages.warning(request,'inavalid credention')
      return render(request,'admnlog.html')
  else:
    return render(request,'admnlog.html')
          
@login_required(login_url='/admin')
def home(request):
  prod=Product.objects.all()
  return render(request,'adhome.html',{'product':prod})
  
        
   
@login_required(login_url='/')    
def productadd(request):
  if request.method =='POST':
    name=request.POST['name']
    product_type=request.POST['product_type']
    product_category=request.POST['product_category'] 
    product_quantity=request.POST['product_quantity']
    attribute =request.POST['attribute']
    price=request.POST['price']
    discount_price=request.POST['discount_price']
    image=request.POST['image']
    prod=Product(image=image,name=name,product_type=product_type,product_category=product_category,product_quantity=product_quantity,attribute=attribute , price= price ,discount_price=discount_price)
    prod.save();
      
    return render(request,'productadd.html')

  return render(request,'productadd.html')





def log(request):
  logout(request)
  return render(request,'admnlog.html')
 
 


@login_required(login_url='/')
def delete(request,id):
     
     product=Product.objects.get(id=id)
     product.delete()
     return redirect('home')

@login_required(login_url='/')
def update(request,id):
  product=Product.objects.get(id=id)
  if request.method=='POST':
    name=request.POST['name']
    product_type=request.POST['product_type']
    product_category=request.POST['product_category']
    product_quantity=request.POST['product_quantity']
    attribute =request.POST['attribute']
    price=request.POST['price']
    discount_price=request.POST['discount_price']
    image=request.POST['image']
    product.name=name
    product.product_type=product_type
    product.product_category=product_category
    product.product_quantity=product_quantity
    product.attribute=attribute
    product.price=price
    product.discount_price=discount_price
    product.image=image
    product.save()
    return redirect(home)

  else:
    return render(request,'update.html',{'product':product})  