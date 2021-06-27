from django.shortcuts import render,redirect, HttpResponseRedirect
from django.http import HttpResponse
from .models import item,category,Order, Customer
from django.contrib.auth.models import User, auth
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.views.generic import ListView
from django.views import View




# Create your views here.
class Index(View):

    def post(self, request):
        item = request.POST.get('item')
        remove =request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(item)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(item)
                    else:    
                        cart[item] = quantity - 1
                else:
                    cart[item] = quantity + 1

            else:
                cart[item] = 1

        else:
            cart = {}
            cart[item] = 1

        request.session['cart'] = cart
        print('cart', request.session['cart'])

        return redirect('/')

    def get(self, request):
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
        item_list = None
        category_list = category.get_all_category()
        CategoryID = request.GET.get('category')
        if CategoryID:
            item_list = item.get_all_items_by_category_id(CategoryID)
        else:
            item_list = item.get_all_items()

        context={}
        context['item_list'] = item_list
        context['category_list'] = category_list
        print('You are ', request.session.get('email'))

        return render(request,'myapp/index.html',context)

        def post(self, request):
            item = request.POST.get('item')
            print(item)

def detail(request,item_id):
    Item = item.objects.get(id=item_id)
    return render(request, 'myapp/detail.html',{'item' : Item})

def add_item(request):
    return render(request, 'myapp/add_item.html')


    return render(request, 'myapp/maincode.html')

class Cart(View):

    def get(self, request):
        ids = list(request.session.get('cart').keys())
        items = item.get_items_by_id(ids)
        return render(request,'myapp/cart.html', {'items' : items})

class Checkout(View):
    
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        items = item.get_items_by_id(list(cart.keys()))
        print(address, phone, customer, cart, items)

        for Item in items:

            order = Order(
                customer = Customer(id = customer),
                item = Item,
                price = Item.price,
                address = address,
                phone = phone,
                quantity = cart.get(str(Item.id)))

            order.save()
        request.session['cart'] = {}

        return redirect('/cart')

class OrderView(View):

    def get(self, request):
        customer = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer)
        print(orders)
        orders = orders.reverse()
        return render(request,'myapp/orders.html',{'orders' : orders})

class Login(View):
    return_url = None
    def get(self, request):
        Login.return_url = request.GET.get('return_url')
        return render(request,'myapp/login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer'] = customer.id
                
                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)

                else:
                    Login.return_url = None
                    return redirect("/")

            else:
                error_message = 'Email or Password invalid !!!'

        else:
            error_message = 'Email or Password invalid !!!'
        print(email, password)
        return render(request, 'myapp/login.html', {'error' : error_message})

def validateCustomer(customer):
    
    error_message = None

    if (not customer.first_name):
        error_message = "First Name Required !!"
    elif len(customer.first_name) < 4:
        error_message = 'First Name must be 4 char long or more'
    elif not customer.last_name:
        error_message = 'Last Name Required'
    elif len(customer.last_name) < 3:
        error_message = 'Last Name must be 3 char long or more'
    elif not customer.phone:
        error_message = 'Phone Number required'
    elif len(customer.phone) < 10:
        error_message = 'Phone Number must be 10 char Long'
    elif len(customer.password) < 6:
        error_message = 'Password must be 6 char long'
    elif len(customer.email) < 5:
        error_message = 'Email must be 5 char long'
    elif customer.isExists():
        error_message = 'Email Address Already Registered.'

    return error_message    

def registerUser(request):
    
        postData = request.POST
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')

        
        #validate 
        value={
            'first_name' : first_name, 
            'last_name' : last_name, 
            'phone' : phone, 
            'email' : email
        }

        error_message = None

        customer = Customer(first_name = first_name, 
                last_name = last_name, 
                phone = phone, 
                email = email, 
                password = password)

        error_message = validateCustomer(customer)

        
       
        #Passing Data and Saving
        if not error_message:
            customer.password = make_password(customer.password)
            customer.register()
            return redirect('/')

        else:   
            data = {
                'error' : error_message,
                'values' : value
            } 
            return render(request, 'myapp/signup.html', data)
     
def signup(request):
    if request.method =='GET':
        return render(request, 'myapp/signup.html')
    else: 
        return registerUser(request)

def logout(request):
    request.session.clear()
    return redirect('/')
