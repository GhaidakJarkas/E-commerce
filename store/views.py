from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime

def store(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    
    else:
        items = []
        order = {"get_cart_total":0, "get_cart_items":0, 'shipping':False}
        cartItems = order['get_cart_items']

    products = Product.objects.all()
    ctx = {'products':products, 'cartItems':cartItems}
    return render(request, "store/store.html", ctx)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    
    else:
        items = []
        order = {"get_cart_total":0, "get_cart_items":0, 'shipping':False}
        cartItems = order['get_cart_items']

    ctx = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, "store/cart.html", ctx)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']

    ctx = {'items':items, 'order':order, 'cartItems':cartItems, 'shipping':False}
    
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
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
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



