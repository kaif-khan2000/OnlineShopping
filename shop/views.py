from django.shortcuts import render,HttpResponse,redirect
from .models import Product,Customer,Order,Cart,Tracker
from django.http import JsonResponse
from django.core import serializers
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
import time
# Create your views here.
def index(request):
    products = Product.objects.all()
    return render(request,'shop/catalog.html',{'products':products})

def signIn(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        status = ""
        if request.is_ajax():
            user = authenticate(username=email,password=password)
        
            if user is not None:
                login(request,user)
                status = 'success'
                print(status)
            else:
                status = 'Authentication failure'
        data = {
            'status':status
        }
        return JsonResponse(data,status=200)

def logoutHandler(request):
    if request.is_ajax:
        logout(request)
    return HttpResponse()

def signUp(request):
    return render(request,'shop/signup.html')

def register(request):
    if request.is_ajax and request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        address = request.POST["address"]
        password = request.POST["password"]

        User.objects.create_user(email,email,password)

        Customer.objects.create(
            name = username,
            email = email,
            address = address,
        )

        return HttpResponse()
def searchHelp(query):
    products = Product.objects.filter(name__icontains = query)
    products = products.union(Product.objects.filter(brand__icontains= query))
    products = products.union(Product.objects.filter(category__icontains= query))
    products = products.union(Product.objects.filter(desc__icontains= query))
    return products;    
def searchRecommendations(request):
    if request.method == "GET" and request.is_ajax:
        query = request.GET['search']
        products = searchHelp(query)
        data = serializers.serialize('json',products)
        return HttpResponse(data,content_type='application/json')

def searchView(request):
    time1 = time.time()
    if request.method == "GET":
        query = request.GET['search']
        queryList = query.split(" ")
        products = searchHelp(query)
        for word in queryList:
            products = products.union(searchHelp(word))
        time2 = time.time()
        total = round(time2-time1,7)
        return render(request,'shop/searchView.html',{'products':products,'query':query,'time':total})
def productView(request,slug):
    product = Product.objects.get(product_id=int(slug))
    other = Product.objects.filter(category__icontains=product.category)
    print(other)
    return render(request,'shop/productView.html',{'product':product,'other':other})

def placeOrder(request):
    if request.method == "GET":
        product_id = request.GET["product_id"]
        userMail = request.user.email
        product = Product.objects.get(product_id = product_id)
        user = Customer.objects.get(email = userMail)
        Order.objects.create(
            customer=user,
            product=product
            
        )
        Tracker.objects.create(
            customer = user,
            product = product
        )
        product.stock -= 1
        product.save()
        return redirect('/orderPage')

def orderPage(request):
    userMail = request.user.email
    user = Customer.objects.get(email = userMail)
    orders = Order.objects.filter(customer=user).order_by('-order_id')

    return render(request,'shop/orders_history.html',{'customer':user,'orders':orders,'pagename':'Orders'})

def addCart(request):
    if request.method == "GET":
        product_id = request.GET["product_id"]
        userMail = request.user.email
        product = Product.objects.get(product_id = product_id)
        user = Customer.objects.get(email = userMail)
        Cart.objects.create(
            customer=user,
            product=product
            
        )
        return redirect("/cartPage")


def cartPage(request):
    userMail = request.user.email
    user = Customer.objects.get(email = userMail)
    orders = Cart.objects.filter(customer=user).order_by('-cart_id')

    return render(request,'shop/orders_history.html',{'customer':user,'orders':orders,'pagename':'Cart'})

def tracker(request,slug):
    userMail = request.user.email
    product_id = int(slug)
    customer = Customer.objects.get(email=userMail)
    product = Product.objects.get(product_id = product_id)

    trackers = Tracker.objects.filter(customer=customer)
    tracker = Tracker.objects.none()
    for tr in trackers:
        if tr.product == product:
            tracker = tr
            break

    listStatus = ['Order Processed','Order Shipped','Order En Route','Order Arrived']
    params = {
        'pre1':'',
        'pre2':'',
        'pre3':'',
        'pre4':'',
        'tracker':tracker,
        'status':listStatus[tracker.status - 1]
    }
    for i in range(1,tracker.status + 1):
        params['pre'+str(i)] = 'active'

    return render(request,'shop/tracker.html',params)