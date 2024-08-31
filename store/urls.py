# store/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('plant_list/', views.plant_list, name='plant_list'),
    path('plant/<int:pk>/', views.plant_detail, name='plant_detail'),
    path('cart/', views.cart_view, name='cart'),
    path('add_to_cart/<int:plant_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('supplier_signup/', views.supplier_signup, name='supplier_signup'),
    path('supplier_login/', views.supplier_login, name='supplier_login'),
    path('', views.supplier_dashboard, name='supplier_dashboard'),
    path('index/', views.index, name='index'),
    path('supplier_signup/', views.supplier_signup, name='supplier_signup'),
    path('supplier_login/', views.supplier_login, name='supplier_login'),
    path('add_plant/', views.add_plant, name='add_plant'),
    path('edit_plant/<int:plant_id>/', views.edit_plant, name='edit_plant'),
    path('delete_plant/<int:plant_id>/', views.delete_plant, name='delete_plant'),
]
