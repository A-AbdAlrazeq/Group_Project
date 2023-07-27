
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('regLog', views.regLog),
    path('register', views.register),
    path('login', views.login),
    path('admin', views.admin),
    path('user', views.user),
    path('add', views.add), 
    path('addCar', views.addCar),
    path('logout', views.logout),
    path('edit/<int:car_id>', views.edit), 
    path('editCar/<int:car_id>', views.editCar),
    path('delete/<int:car_id>', views.delete),
    path('addToCart/<int:car_id>', views.view_cart),
    path('addToCart2/<int:car_id>', views.add_to_cart),
    path('cart', views.cart),	  
    path('checkout', views.checkout), 
    path('add_favorite/<int:car_id>', views.add_to_favorites),
    path('remove_favorite/<int:car_id>', views.remove_from_favorites),
     path('remove_cart/<int:car_id>', views.remove_car_from_cart),
    path('bookmark', views.show_favorites),
]