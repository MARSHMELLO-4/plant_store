from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from .models import Plant, Category, Cart, CartItem, Order, Supplier
from .forms import CustomerSignUpForm, SupplierSignUpForm, CustomerUpdateForm, SupplierUpdateForm, PlantForm
from .decorators import supplier_required

def index(request):
    return render(request, 'store/index.html')

# Plant list view
def plant_list(request):
    categories = Category.objects.all()
    plants = Plant.objects.all()
    return render(request, 'store/plant_list.html', {'categories': categories, 'plants': plants})

# Plant detail view
@login_required
def plant_detail(request, pk):
    plant = get_object_or_404(Plant, pk=pk)
    return render(request, 'store/plant_detail.html', {'plant': plant})

# Login view
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

# Signup view
def signup(request):
    if request.method == 'POST':
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomerSignUpForm()
    return render(request, 'store/signup.html', {'form': form})

# Logout view
def logout_view(request):
    auth_logout(request)
    return redirect('index')

# Add to cart view
@login_required
def add_to_cart(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, plant=plant)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('cart')

# Cart view
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

# Remove from cart view
@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect('cart')

# Update cart view
@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
    return redirect('cart')

# Supplier signup view
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

# Supplier login view
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

# Supplier dashboard view
@login_required
@supplier_required
def supplier_dashboard(request):
    supplier = request.user.supplier
    plants = supplier.plants.all()
    orders = Order.objects.filter(plant__supplier=supplier)
    context = {
        'supplier': supplier,
        'orders': orders,
        'plants': plants,
    }
    return render(request, 'store/supplier_dashboard.html', context)

# Supplier add plant view
@login_required
@supplier_required
def add_plant(request):
    supplier = request.user.supplier
    if request.method == 'POST':
        form = PlantForm(request.POST, request.FILES)
        if form.is_valid():
            plant = form.save(commit=False)
            plant.supplier = supplier
            plant.save()
            return redirect('supplier_dashboard')
    else:
        form = PlantForm()
    return render(request, 'store/add_plant.html', {'form': form})

# Supplier edit plant view
@login_required
@supplier_required
def edit_plant(request, plant_id):
    supplier = request.user.supplier
    plant = get_object_or_404(Plant, id=plant_id, supplier=supplier)
    if request.method == 'POST':
        form = PlantForm(request.POST, request.FILES, instance=plant)
        if form.is_valid():
            form.save()
            return redirect('supplier_dashboard')
    else:
        form = PlantForm(instance=plant)
    return render(request, 'store/edit_plant.html', {'form': form, 'plant': plant})

# Supplier delete plant view
@login_required
@supplier_required
def delete_plant(request, plant_id):
    supplier = request.user.supplier
    plant = get_object_or_404(Plant, id=plant_id, supplier=supplier)
    if request.method == 'POST':
        plant.delete()
        return redirect('supplier_dashboard')
    return render(request, 'store/delete_plant.html', {'plant': plant})

# Update customer details view
@login_required
def update_customer_details(request):
    customer = request.user.customer
    if request.method == 'POST':
        form = CustomerUpdateForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('plant_list')
    else:
        form = CustomerUpdateForm(instance=customer)
    return render(request, 'store/update_customer_details.html', {'form': form})

# Update supplier details view
@login_required
@supplier_required
def update_supplier_details(request):
    supplier = request.user.supplier
    if request.method == 'POST':
        form = SupplierUpdateForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('supplier_dashboard')
    else:
        form = SupplierUpdateForm(instance=supplier)
    return render(request, 'store/update_supplier_details.html', {'form': form})

# Place order view
@login_required
def place_order(request):
    user = request.user
    cart = Cart.objects.get(user=user)
    cart_items = CartItem.objects.filter(cart=cart)

    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('cart')

    try:
        with transaction.atomic():
            for item in cart_items:
                plant = item.plant
                quant = item.quantity
                order = Order.objects.create(
                    customer=user.customer,
                    plant=plant,
                    quantity=quant,
                )
            cart_items.delete()  # Clear the cart after placing the order
        messages.success(request, "Order placed successfully!")
        return redirect('order_success')
    except Exception as e:
        messages.error(request, f"An error occurred while placing the order: {str(e)}")
        return redirect('cart')

# Order success view
@login_required
def order_success(request):
    return render(request, 'store/order_success.html')

# Complete customer profile view
@login_required
def complete_profile(request):
    customer = request.user.customer
    if request.method == 'POST':
        form = CustomerUpdateForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile completed successfully!")
            return redirect('plant_list')
    else:
        form = CustomerUpdateForm(instance=customer)
    return render(request, 'store/complete_profile.html', {'form': form})
