from django.urls import path

from .views import dashboard,customer,products

app_name = 'accounts'

urlpatterns = [
    path('dashboard/',dashboard,name='dashboard'),
    path('customer/<int:pk>/',customer,name='customer'),
    path('products/',products,name='products'),
]