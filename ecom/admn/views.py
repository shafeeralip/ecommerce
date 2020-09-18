from django.shortcuts import render,redirect
from django.contrib import messages
from prod.models import Product

# Create your views here.

def admn(request):
  if request.session.has_key('username'):
    return render(request,'admnhome.html')
  else:
    return render(request,'admnlog.html')
  
   

def home(request):
  if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        if username=='shafeer' and password=='123':
            request.session['username']=username
            prod=Product.objects.all()
            return render(request,'admnhome.html',{'product':prod})
        else:
            messages.error(request,'invalid credential')
            return render (request,'admnlog.html')

   
    
def addproduct(request):
  return render(request,'addproduct.html')
# def delete(request,id):
     
#      product=Product.objects.get(id=id)
#      product.delete()
#      return redirect('home')

# def update(request,id):
#     product=Product.objects.get(id=id)
#     if request.method=='POST':
#         first_name=request.POST['first_name']
#         last_name=request.POST['last_name']
#         email=request.POST['email']
#         product.first_name=first_name
#         product.last_name=last_name
#         product.email=email
#         product.save();
#         return redirect('home')


#     else:
#         return render(request,'update.html',{'user':product})  