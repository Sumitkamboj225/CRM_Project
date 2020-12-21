from django.shortcuts import render,redirect
from .models import Customers,Orders,Products
from .forms import OrderForm,CustomerFrom,ProductForm,CreateUserForm,CustomerOrderForm
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user,allowed_user,admin_only,product_decorator

@unauthenticated_user
def register_view(request):
    form=CreateUserForm()
    if request.method=="POST":
        form=CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            #user = request.POST.get('username')
            messages.success(request,"User Registered Successfully.")
            return redirect('login')
        else:
            messages.error(request,'Enter all details..')
    context={'form':form}
    return render(request,'accounts/register.html',context)

@unauthenticated_user
def login_view(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Enter valid user and password...')
    return render(request,'accounts/login.html')

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@allowed_user(allowed_role=['customer'])
def userpage(request):
    customers=Customers.objects.get(user=request.user)
    orders=request.user.customers.orders_set.all().order_by('-created_date')
    total_orders = len(orders)
    pending_orders = orders.filter(status="Pending").count()
    delivered_orders = orders.filter(status="Delivered").count()
    outfordelivery = orders.filter(status="OutForDelivery").count()

    context={'customer':customers,'orders':orders,'total_orders':total_orders,'pending_orders':pending_orders,'delivered_orders':delivered_orders,'outfordelivery':outfordelivery}
    return render(request,'accounts/user-page.html',context)

@login_required(login_url='login')
@admin_only
def home(request):
        customers = Customers.objects.all()
        orders = Orders.objects.all()
        cust_orders = Orders.objects.order_by('-created_date')[0:5]
        total_orders = len(orders)
        pending_orders = orders.filter(status="Pending").count()
        delivered_orders = orders.filter(status="Delivered").count()
        outfordelivery = orders.filter(status="OutForDelivery").count()
        context = {'customers': customers, 'orders': cust_orders, 'total_orders': total_orders,
                   'pending_orders': pending_orders, 'delivered_orders': delivered_orders,
                   'outfordelivery': outfordelivery}
        return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='login')
@product_decorator
def products(request):
    products=Products.objects.all()
    context={'products':products}
    return render(request,'accounts/products.html',context)

@login_required(login_url='login')
def customer(request,str_pk):
    customer=Customers.objects.get(id=str_pk)
    orders=customer.orders_set.all()
    total_orders=len(orders)
    context={'customer':customer,'orders':orders,'total_orders':total_orders}
    return render(request,'accounts/customers.html',context)

@login_required(login_url='login')
def update_order(request,pk):
    order=Orders.objects.get(id=pk)
    form=OrderForm(instance=order)
    if request.method=="POST":
        form=OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context={'form':form}
    return render(request,'accounts/update_order.html',context)

@login_required(login_url='login')
def delete_order(request,pk):
    order=Orders.objects.get(id=pk)
    order.delete()
    return redirect('/')

@login_required(login_url='login')
def create_order2(request,customer):
    if customer:
        form=CustomerOrderForm
        if request.method=="POST":
            form=CustomerOrderForm(request.POST)
            if form.is_valid():
                coform=form.save(commit=False)
                coform.customer=request.user.customers
                coform.save()
                return redirect('/')
    else:
        form=OrderForm()
        if request.method=="POST":
            form=OrderForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/')
    context={'form':form}
    return render(request,'accounts/create_order.html',context)

@login_required(login_url='login')
def update_customer(request,pk):
    customer=Customers.objects.get(id=pk)
    form=CustomerFrom(instance=customer)
    if request.method=="POST":
        form=CustomerFrom(request.POST,instance=customer)
        if form.is_valid():
            form.save()
            return redirect('/')
    context={'form':form}
    return render(request,'accounts/update_customer.html',context)

@login_required(login_url='login')
def delete_customer(request,pk):
    customer=Customers.objects.get(id=pk)
    customer.delete()
    return redirect('/')

@login_required(login_url='login')
def update_product(request,pk):
    product=Products.objects.get(id=pk)
    form=ProductForm(instance=product)
    if request.method=="POST":
        form=ProductForm(request.POST,instance=product)
        if form.is_valid():
            form.save()
            return redirect('/')
    context={'form':form}
    return render(request,'accounts/update_product.html',context)

@login_required(login_url='login')
def delete_product(request,pk):
    product=Products.objects.get(id=pk)
    product.delete()
    return redirect('/')

@login_required(login_url='login')
def create_order(request):
    if customer:
        form=OrderForm
        if request.method=="POST":
            form=OrderForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/')
    else:
        form=OrderForm()
        if request.method=="POST":
            form=OrderForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/')
    context={'form':form}
    return render(request,'accounts/create_order.html',context)
