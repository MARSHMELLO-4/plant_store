# store/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Plant, Category, Cart, CartItem
from django.contrib.auth.decorators import login_required

def plant_list(request):
    categories = Category.objects.all()
    plants = Plant.objects.all()
    return render(request, 'store/plant_list.html', {'categories': categories, 'plants': plants})

def plant_detail(request, pk):
    plant = get_object_or_404(Plant, pk=pk)
    return render(request, 'store/plant_detail.html', {'plant': plant})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('plant_list')
    else:
        form = AuthenticationForm()
    return render(request, 'store/login.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'store/signup.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    return redirect('plant_list')

@login_required
def add_to_cart(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, plant=plant)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('cart')

@login_required
def cart_view(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total = sum(item.plant.price * item.quantity for item in cart_items)
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'store/cart.html', context)

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect('cart')

@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
    return redirect('cart')


from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from .forms import SupplierSignUpForm

def supplier_signup(request):
    if request.method == 'POST':
        form = SupplierSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('supplier_dashboard')
    else:
        form = SupplierSignUpForm()
    return render(request, 'store/supplier_signup.html', {'form': form})

def supplier_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('supplier_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'store/supplier_login.html', {'form': form})

def supplier_dashboard(request):
    return render(request, 'store/supplier_dashboard.html')

def index(request):
    return render(request, 'store/index.html')
