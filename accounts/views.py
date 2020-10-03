from django.shortcuts import render

# Create your views here.
def dashboard(request):
    return render(request,'accounts/dashboard.html')

def profile(request):
    pass

def products(request):
    return render(request,'accounts/products.html')

def customer(request):
    return render(request,'accounts/customer.html')