from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name="home"),
    path('product',views.products,name="product"),
    path('customers/<str_pk>',views.customer,name="customer"),
    path('home',views.home),
    path('update_order/<pk>',views.update_order,name="update_order"),
    path('delete_order/<pk>',views.delete_order,name="delete_order"),
    path('create_order',views.create_order,name='create_order'),
    path('update_customer/<pk>',views.update_customer,name="update_customer"),
    path('delete_customer/<pk>',views.delete_customer,name="delete_customer"),
    path('udpate_product/<pk>',views.update_product,name="update_product"),
    path('delete_product/<pk>',views.delete_product,name='delete_product'),
    path('register/',views.register_view,name="register"),
    path('login/',views.login_view,name="login"),
    path('logout/',views.logout_view,name="logout"),
    path('user/',views.userpage,name='user-page'),
    path('create_order2/<str:customer>',views.create_order2,name='customer_order2'),
]
