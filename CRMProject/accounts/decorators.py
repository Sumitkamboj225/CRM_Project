from django.http.response import HttpResponse
from django.shortcuts import redirect,render

def unauthenticated_user(view_func):
    def wrapper_fun(request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request,*args,*kwargs)
    return wrapper_fun

def allowed_user(allowed_role=[]):
    def decorator(view_func):
        def wrapper_func(request,*args,**kwargs):
            group=None
            if request.user.groups.exists():
                group=request.user.groups.all()[0].name
            if group in allowed_role:
                return view_func(request,*args,**kwargs)
            else:
                return redirect('user-page')
        return wrapper_func
    return decorator

def admin_only(view_func):
    def wrapper_func(request,*args,**kwargs):
        group=None
        if request.user.groups.exists():
            group=request.user.groups.all()[0].name
        if group=='customer':
            return redirect('user-page')
        if group=='admin':
            return view_func(request,*args,**kwargs)
    return wrapper_func

def product_decorator(view_func):
    def wrapper_func(request,*args,**kwargs):
        group=None
        if request.user.groups.exists():
            group=request.user.groups.all()[0].name
        if group=='admin':
            return view_func(request,*args,**kwargs)
        else:
            return HttpResponse("You are not authorized user to see this page.")
    return wrapper_func