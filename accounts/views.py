from django.shortcuts import render,redirect
from .models import Customer,Product,Order,tag
from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from .forms import OrderForm,CreateUserForm,CustomerForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user,allowed_users,admin_only
from django.contrib.auth.models import Group
# Create your views here.
@unauthenticated_user
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()

            add_group = Group.objects.get(name='customer')
            user.groups.add(add_group)
            Customer.objects.add(user=user)

            username = form.cleaned_data.get('username')
            messages.success(request,f'Account was created for {username}')

            return redirect('accounts:login')
    context ={'form':form}
    return render(request,'accounts/register.html',context)

@unauthenticated_user
def loign(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('accounts:dashboard')
        else:
            messages.info(request,'User or Password is incorrect')

    context ={}
    return render(request,'accounts/login.html',context)

def UserLogout(request):
    logout(request)
    return redirect('accounts:login')

@login_required(login_url='accounts:login')
@admin_only
def dashboard(request):
    orders = Order.objects.all().order_by('-date_created')
    customers = Customer.objects.all()
    total_orders = orders.count()
    total_delivered = orders.filter(status='Delivered').count()
    total_pending = orders.filter(status='Pending').count()
    context ={
        'customers':customers,
        'orders':orders,
        'total_orders':total_orders,
        'total_delivered':total_delivered,
        'total_pending':total_pending,
    }
    return render(request,'accounts/dashboard.html',context)

@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['customer'])
def profile(request):
    orders = request.user.customer.order_set.all()

    total_orders = orders.count()
    total_delivered = orders.filter(status='Delivered').count()
    total_pending = orders.filter(status='Pending').count()

    context={
        'orders':orders,
        'total_orders':total_orders,
        'total_delivered':total_delivered,
        'total_pending':total_pending,
        }
    return render(request,'accounts/user.html',context)

@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['customer'])
def accountsettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method =='POST':
        form = CustomerForm(request.POST,request.FILES,instance=customer)
        if form.is_valid():
            form.save()

    context={
        'form':form,
    }
    return render(request,'accounts/account_settings.html',context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    context = {
        'products':products,
    }
    return render(request,'accounts/products.html',context)
@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def customer(request,pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    total_orders = orders.count()

    search = OrderFilter(request.GET,queryset=orders)
    orders = search.qs


    context={
        'customer':customer,
        'orders':orders,
        'total_orders':total_orders,
        'search':search,
    }
    return render(request,'accounts/customer.html',context)
@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def order_create(request,pk):
    OrderFormSet = inlineformset_factory(Customer,Order,fields=('product','status'),extra=2)
    customer = Customer.objects.get(id=pk)
    # formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
    form = OrderForm(initial={'customer':customer})
    if request.method =='POST':
        form = OrderForm(request.POST)
        # formset = OrderFormSet(request.POST,instance=customer)
        # if formset.is_valid():
        if form.is_valid():
            # formset.save()
            form.save()
            return redirect('accounts:dashboard')
    context ={
        # 'formset':formset,
        'form':form,
    }
    return render(request,'accounts/order_form.html',context)
@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def order_update(request,pk):
    
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method =='POST':
        form = OrderForm(request.POST,instance=order)
        if form.is_valid:
            form.save()
            return redirect('accounts:dashboard')
    context = {
        'form':form
    }
    return render(request,'accounts/order_form.html',context)
@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def order_delete(request,pk):
    order = Order.objects.get(id=pk)
    if request.method  == 'POST':
        order.delete()
        return redirect('accounts:dashboard')
    context = {
        'order':order
    }
    return render(request,'accounts/order_delete.html',context)


