from django.shortcuts import render,redirect
from django.contrib import messages
from prod.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout
from django.views.decorators.cache import cache_control
from django.core.files.storage import FileSystemStorage
from datetime import *
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test

# Create your views here.

def admn(request):
  if request.user.is_authenticated and request.user.is_superuser:
    prod=Product.objects.all()
    return redirect(home)
  elif request.method =='POST':
    username=request.POST['username']
    password=request.POST['password']
    user=authenticate(username=username,password=password)
    if user:
        if username =='shafee' and password =='123':
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
          
@user_passes_test(lambda u: u.is_superuser,login_url='/admin')
def home(request):

  year = datetime.now().year
  month = datetime.now().month
  today=date.today()
  print("hello",today)

  
  values = []
  for i in range(0,12):
    chart_order = Order.objects.filter(date_orderd__year = year,date_orderd__month = i)
    order_total = 0
    for items in chart_order:
        try:
            order_total += round(items.get_cart_total,2)
        except:
            order_total += 0
    values.append(round(order_total,2))  
        
  # print(chart_values)
 
  
  orders = Order.objects.all()
  total_income = 0
  for order in orders:
    try:
      order_total = order.get_cart_total
    except:
      order_total = 0
    total_income = total_income + order_total

  today_order=Order.objects.filter(date_orderd__date = today,complete=True)
  print("hi",today_order)
  today_income=0
  for order in today_order:
    try:
      order_total = order.get_cart_total
    except:
      order_total = 0
    today_income = today_income + order_total

  customer=Customer.objects.all()

  

  return render(request,'dashbord.html',{'values':values,'total_income':total_income,'today_order':today_order,'today_income':today_income,'customer':customer})

  
        
   
@user_passes_test(lambda u: u.is_superuser,login_url='/')    
def productadd(request):
  pd=Product.objects.all()
  if request.method =='POST':
    name=request.POST['name']
    product_type=request.POST['product_type']
    product_category=request.POST['product_category'] 
    product_quantity=request.POST['product_quantity']
    attribute =request.POST['attribute']
    price=request.POST['price']
    
    image=request.FILES.get('myfile')
    prod=Product(image=image,name=name,product_type=product_type,product_category=product_category,product_quantity=product_quantity,attribute=attribute , price= price)
    prod.save();
      
    return redirect('/admin/adproduct')

  return render(request,'productadd.html',{'pd':pd})





def log(request):
  logout(request)
  return render(request,'admnlog.html')
 
 


@user_passes_test(lambda u: u.is_superuser,login_url='/')
def delete(request,id):
     
     product=Product.objects.get(id=id)
     product.delete()
     return redirect('home')

@user_passes_test(lambda u: u.is_superuser,login_url='/')
def update(request,id):
  product=Product.objects.get(id=id)
  if request.method=='POST':
    name=request.POST['name']
    product_type=request.POST['product_type']
    product_category=request.POST['product_category']
    product_quantity=request.POST['product_quantity']
    attribute =request.POST['attribute']
    price=request.POST['price']
    product.name=name
    product.product_type=product_type
    product.product_category=product_category
    product.product_quantity=product_quantity
    product.attribute=attribute
    product.price=price
    if 'image' not in request.POST:
      image=request.POST['image']
    else:
      image=product.image
       
    product.image=image
    product.save()
    return redirect('/admin/adproduct')

  else:
    return render(request,'update.html',{'product':product})  


@user_passes_test(lambda u: u.is_superuser,login_url='/')
def adproduct(request):
  prod=Product.objects.all()
  return render(request,'adproduct.html',{'product':prod})

@user_passes_test(lambda u: u.is_superuser,login_url='/')
def order(request):
  order=Order.objects.all()
   
  return render(request,'adorder.html',{'order':order})
 
 

@user_passes_test(lambda u: u.is_superuser,login_url='/') 
def approve(request,id):

  if request.method=='POST':

    order=Order.objects.get(id=id)
    order.value=request.POST['status']
    print("hi",order.value)

    order.save();
    return redirect('order')
    
  order=Order.objects.all()
  return render(request,'adorder.html',{'order':order})




  # if order.approve==False:
  #   order.approve=True
   
  # elif order.approve==True:
  #   order.approve=False
  
  
  

@user_passes_test(lambda u: u.is_superuser,login_url='/')
def customer(request):
  
  customer=Customer.objects.all()
  item=[]
  for cu in customer:
    order=Order.objects.filter(customer=cu,complete=True)
    value=order.count()
    item.append(value)
  
  print("itms:",item)
    

  values=zip(customer,item)
 
  return render(request,'adcustomer.html',{'value':values})

@login_required(login_url='/')   
def customerdel(request,id):
  customer=Customer.objects.get(id=id)
  customer.delete()
  return redirect('/admin/customer')

@login_required(login_url='/') 
def user(request):
  user=User.objects.all()
  return render(request,'aduser.html',{'user':user})




  
      

        
      

      

      

   
   
    
  


  


  
 

    

  
