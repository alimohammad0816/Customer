from django.urls import path

from .views import dashboard,customer,products,order_create,order_update,order_delete,register,loign,UserLogout,profile

app_name = 'accounts'

urlpatterns = [
    path('register/',register,name='register'),
    path('login/',loign,name='login'),
    path('logout/',UserLogout,name='logout'),

    path('profile/',profile,name='profile'),
    path('dashboard/',dashboard,name='dashboard'),
    path('products/',products,name='products'),
    path('customer/<int:pk>/',customer,name='customer'),

    path('create/<int:pk>',order_create,name='order_create'),
    path('update/<int:pk>',order_update,name='order_update'),
    path('delete/<int:pk>',order_delete,name='order_delete'),
]