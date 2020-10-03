from django.shortcuts import render,redirect
from .models import Customer,Product,Order,tag
from .forms import OrderForm

# Create your views here.
def dashboard(request):
    orders = Order.objects.all()
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

def profile(request):
    pass

def products(request):
    products = Product.objects.all()
    context = {
        'products':products,
    }
    return render(request,'accounts/products.html',context)

def customer(request,pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    total_orders = orders.count()
    context={
        'customer':customer,
        'orders':orders,
        'total_orders':total_orders,
    }
    return render(request,'accounts/customer.html',context)

def order_create(request):
    form = OrderForm()
    if request.method =='POST':
        form = OrderForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('accounts:dashboard')
    context ={'form':form}
    return render(request,'accounts/order_form.html',context)

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

def order_delete(request,pk):
    order = Order.objects.get(id=pk)
    if request.method  == 'POST':
        order.delete()
        return redirect('accounts:dashboard')
    context = {
        'order':order
    }
    return render(request,'accounts/order_delete.html',context)