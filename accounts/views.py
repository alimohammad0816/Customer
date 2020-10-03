from django.shortcuts import render
from .models import Customer,Product,Order,tag

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

def customer(request):
    return render(request,'accounts/customer.html')