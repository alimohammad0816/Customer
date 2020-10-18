from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(views_func):
    def wrapper_func(request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('accounts:dashboard')
        else:
            return views_func(request,*args,**kwargs)
    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(views_func):
        def wrapper_func(request,*args,**kwargs):
            
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return views_func(request,*args,**kwargs)
            else:
                return HttpResponse('You are not authorized to view')
            
        return wrapper_func
    return decorator

def admin_only(views_func):
    def wrapper_func(request,*args,**kwargs):
            
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'customer':
            return redirect('accounts:profile')
        if group == 'admin':
            return views_func(request,*args,**kwargs)
    return wrapper_func