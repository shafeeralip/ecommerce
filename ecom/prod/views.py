from django.shortcuts import render,redirect
from . models import *
from django.contrib.auth.models import auth,User
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ca.utils import cookieCart,cartData
from django.contrib.auth import authenticate, login,logout
import json
import requests
import razorpay
from datetime import *
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

def orders(request):
    data = cartData(request)
    cartItems=data['cartItems']
    customer=request.user.customer
    orders =Order.objects.filter(customer=customer,complete=True)
    items=[]
    try:
        for order in orders:
            orderitems=OrderItem.objects.filter(order=order)
            for orderitem in orderitems:
                items.append(orderitem)
            

        
    except:
        order=0
        items=0
    
    zipitems=zip(items,orders)
    
    return render(request,'userorder.html',{'zipitems':zipitems,'cartItems':cartItems})

def userlogin(request):
    if request.user.is_authenticated:
        return redirect(home)

    elif request.method =='POST':
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
    if request.user.is_authenticated:
        return redirect(home)
    elif request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        number=request.POST['number']
        dicti = {"username":username,"email":email}
        if User.objects.filter(username=username).exists():
            messages.info(request,'username already taken')
            return render(request, "login.html", dicti)
        elif User.objects.filter(email=email).exists():
            messages.info(request,'email already taken')
            return render(request, "login.html", dicti)
        elif User.objects.filter(last_name=number).exists():
            messages.info(request,'mobail number already taken')
            return render(request, "login.html", dicti)

        else:
            
            request.session['username'] =  username
            request.session['password'] = password
            request.session['email']=email
            request.session['number']=number

            

            url = "https://d7networks.com/api/verifier/send"
            number=str(91) + number
            
            payload = {'mobile': number,
            'sender_id': 'SMSINFO',
            'message': 'Your otp code is {code}',
            'expiry': '900'}
            files = [

            ]
            headers = {
            'Authorization': 'Token ae88b588f853eccd3e1b1c8befd530c5d68c47ea'
            }

            response = requests.request("POST", url, headers=headers, data = payload, files = files)

            print(response.text.encode('utf8'))
            data=response.text.encode('utf8')
            datadict=json.loads(data.decode('utf-8'))

            id=datadict['otp_id']
            status=datadict['status']
            print('id:',id)
            request.session['id'] = id
        
            return render(request,'otp.html')

            
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
    try:
        url = "https://restcountries-v1.p.rapidapi.com/all"
        headers = {
        'x-rapidapi-host': "restcountries-v1.p.rapidapi.com",
        'x-rapidapi-key': "a1adc67eb8msh45ba3862e81291ap103047jsn91937edcd3b3"
        }

        response = requests.request("GET", url, headers=headers)

        
        country=json.loads(response.text)
        cont=[]
        for c in country:

            con= c['name']
            cont.append(con)
            
            

        # for country in country:
            
        

    
        client=razorpay.Client(auth=("rzp_test_7i01eG7knm1628","K9H5VQX0OHOsFwPMDY8DCMzp"))
        data = cartData(request)
        cartItems=data['cartItems']
        order=data['order']
        items=data['items']
        order_currency='USD'
        order_receipt = 'order-rctid-11'

        if request.user.is_authenticated:
            
            order_amount=order.get_cart_total
            order_amount *= 100
        
        else:
        
            order_amount=order['get_cart_total']
            order_amount *= 100
            
        


        response = client.order.create(dict(
            amount=order_amount,
            currency=order_currency,
            receipt=order_receipt,
            payment_capture='0'
            
            ))
        
        order_id=response['id']
        context = {'items':items,'order':order,'cartItems':cartItems,'order_id':order_id,'cont':cont}
        return render(request,'checkout.html',context)
        
    except:
        pass

    return render(request,'checkout.html')
    
    
    


def mobail(request):

    if request.method=='POST':
        number = request.POST['number']
        user=User.objects.get(last_name=number)
        print(user)
       
        if user:
            username = user.username
            password=user.first_name
            request.session['username'] =  username
            request.session['password'] = password
            

            url = "https://d7networks.com/api/verifier/send"
            number=str(91) + number
            
            payload = {'mobile': number,
            'sender_id': 'SMSINFO',
            'message': 'Your otp code is {code}',
            'expiry': '900'}
            files = [

            ]
            headers = {
            'Authorization': 'Token ae88b588f853eccd3e1b1c8befd530c5d68c47ea'
            }

            response = requests.request("POST", url, headers=headers, data = payload, files = files)

            print(response.text.encode('utf8'))
            data=response.text.encode('utf8')
            datadict=json.loads(data.decode('utf-8'))

            id=datadict['otp_id']
            status=datadict['status']
            print('id:',id)
            request.session['id'] = id
           
            return render(request,'otp.html')

        else:
            messages.info(request,'mobail number not registerd')
            return render(request,'mobail.html')

            
            
        
# {"otp_id":"6939d5de-8517-4788-b556-054404497e8d","status":"open","expiry":900}'

            
    return render(request,'mobail.html')



def otp(request):
    if request.method=='POST':
        otp=request.POST['otp']
       
        id=request.session['id']
        url = "https://d7networks.com/api/verifier/verify"

        payload = {'otp_id': id,
        'otp_code': otp}
        files = [

        ]
        headers = {
        'Authorization': 'Token ae88b588f853eccd3e1b1c8befd530c5d68c47ea'
        }

        response = requests.request("POST", url, headers=headers, data = payload, files = files)

        print(response.text.encode('utf8'))
        data=response.text.encode('utf8')
        datadict=json.loads(data.decode('utf-8'))
        status=datadict['status']
        
        if status=='success':
            
            username = request.session['username']   
            password =  request.session['password']
            if User.objects.filter(username=username).exists():
                user=authenticate(username=username,password=password)

               
            else:
                email=request.session['email']
                number=request.session['number']
                user=User.objects.create_user(username=username,email=email,password=password,last_name=number,first_name=password)
                user.save();

            login(request,user)

            return redirect(home)


                

        
        else:
            messages.info(request,'incorrectotp')
            return render(request,'otp.html')



        

    return render(request,'otp.html')