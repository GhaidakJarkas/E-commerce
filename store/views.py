from decimal import Decimal
from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime
from store.utilis import cartData, cookieCart, guestOrder

def store(request):
    products = Product.objects.all()
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']
    ctx = {'items':items, 'order':order, 'cartItems':cartItems, 'products':products}
    return render(request, "store/store.html", ctx)

def cart(request):
    
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']
    ctx = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, "store/cart.html", ctx)

def checkout(request):
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']
    ctx = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, "store/checkout.html", ctx)


def update_item(request):
    data = json.loads(request.body)
    productID = data['productID']
    action = data['action']
    customer = request.user.customer
    product = Product.objects.get(id=productID)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderitem, created = OrderItem.objects.get_or_create(order=order, product=product)
    if action == "add":
        orderitem.quantity += 1
    else:
        orderitem.quantity -= 1
    orderitem.save()
    if orderitem.quantity <= 0:
        orderitem.delete()
    return JsonResponse('Data was added to the cart', safe=False)


def proccessOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)        

    else:
        customer, order = guestOrder(request, data)
    
    total = Decimal(data['form']['total'])
    order.transaction_id = transaction_id
    
    if total == order.get_cart_total:
        print('total is assessed')
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer = customer,
            order = order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zipcode = data['shipping']['zip']
        )



    return JsonResponse("Payment Complete", safe=False) 



