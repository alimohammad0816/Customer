from django.urls import path

from .views import dashboard,customer,products,order_create,order_update,order_delete

app_name = 'accounts'

urlpatterns = [
    path('dashboard/',dashboard,name='dashboard'),
    path('customer/<int:pk>/',customer,name='customer'),
    path('products/',products,name='products'),
    path('create/',order_create,name='order_create'),
    path('create/<int:pk>',order_update,name='order_update'),
    path('delete/<int:pk>',order_delete,name='order_delete'),
]