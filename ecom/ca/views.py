from django.shortcuts import render,redirect
from prod.models import *
from django.http import JsonResponse
import json
from .utils import guestUser,cartData
import datetime


# from cart.cart import Cart


# Create your views here.

def cart_detail(request):
    data = cartData(request)

    cartItems=data['cartItems']
    order=data['order']
    items=data['items']
    
    context = {'items':items,'order':order,'cartItems':cartItems}
    return render(request,'cart.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('action;',action)
    print('productId :',productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order,created =Order.objects.get_or_create(customer=customer,complete=False)
    orderItem,created =OrderItem.objects.get_or_create(order=order,product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity =(orderItem.quantity - 1)
    
    orderItem.save()

    if orderItem.quantity <=0:
        orderItem.delete()
    
    elif action =='delete':
        orderItem.delete()

    
    return JsonResponse('item was added',safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order,created =Order.objects.get_or_create(customer=customer,complete=False)
        

    else:
        customer , order = guestUser(request,data)  
    
    total = data['form']['total']
    order.transaction_id = transaction_id

    if float(total) == float(order.get_cart_total) :
        order.complete = True

    order.save()

    if order.shipping == True:
        ShippingAdress.objects.create(
            customer=customer,
            order = order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zipcode = data['shipping']['zipcode'],
            
        )


    return JsonResponse('payment complete',safe=False)




# def cart_detail(request):
#     if request.COOKIES.get('user'):
#         return render(request,'cart.html')
#     return render(request,'login.html')
    
        
    

# def cart_add(request, id):
#     cart = Cart(request)
#     product = Product.objects.get(id=id)
#     cart.add(product=product)
#     return redirect("/")


# def cart_adding(request, id):
#     cart = Cart(request)
#     product = Product.objects.get(id=id)
#     cart.add(product=product)
#     return redirect('/prodv/%d/' %product.id)


# def item_clear(request, id):
#     cart = Cart(request)
#     product = Product.objects.get(id=id)
#     cart.remove(product)
#     return redirect(cart_detail)

# def item_increment(request, id):
#     cart = Cart(request)
#     product = Product.objects.get(id=id)
#     cart.add(product=product)
#     return redirect("cart_detail")

# def item_decrement(request, id):
#     cart = Cart(request)
#     product = Product.objects.get(id=id)
#     cart.decrement(product=product)
#     return redirect("cart_detail")

# def cart_clear(request):
#     cart = Cart(request)
#     cart.clear()
#     return redirect("cart_detail")
