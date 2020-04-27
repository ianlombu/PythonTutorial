from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('user/', views.userPage, name="user-page"),
    path('product/', views.product, name='product'),
    path('customer/<str:id>', views.customer, name='customer'),
    path('create_order/<str:id>', views.createOrder, name='create_order'),
    path('update_order/<str:id>', views.updateOrder, name='update_order'),
    path('delete_order/<str:id>', views.deleteOrder, name='delete_order'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register')
]
