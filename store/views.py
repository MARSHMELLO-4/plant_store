# store/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Plant, Category, Cart, CartItem
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import SupplierSignUpForm, PlantForm
from .models import Supplier, Plant
from .decorators import supplier_required
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from .forms import SupplierSignUpForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Customer, Supplier
from .forms import CustomerUpdateForm, SupplierUpdateForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Plant, Order, Customer
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import CustomerSignUpForm, SupplierSignUpForm
#index
def index(request):
    return render(request, 'store/index.html')

#plant list 
def plant_list(request):
    categories = Category.objects.all()
    plants = Plant.objects.all()
    return render(request, 'store/plant_list.html', {'categories': categories, 'plants': plants})

#plant detail
@login_required
def plant_detail(request, pk):
    plant = get_object_or_404(Plant, pk=pk)
    return render(request, 'store/plant_detail.html', {'plant': plant})

#login view 
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

#signup view 
def signup(request):
    if request.method == 'POST':
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login after successful sign-up
    else:
        form = CustomerSignUpForm()
    return render(request, 'store/signup.html', {'form': form})

#logoutview
def logout_view(request):
    auth_logout(request)
    return redirect('index')

#loginview
@login_required
def add_to_cart(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, plant=plant)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('cart')

#cartview
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

#remove from cart
@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect('cart')

#update card
@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
    return redirect('cart')

#supplier signup
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

#supplier login
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

#supplier dashboard
def supplier_dashboard(request):
    # Ensure the user is a supplier
    supplier = request.user.supplier
    plants = supplier.plants.all()
    orders = Order.objects.filter(plant__supplier=supplier)  # Get all orders related to this supplier
    context = {
        'supplier': supplier,
        'orders': orders
    }
    return render(request, 'store/supplier_dashboard.html', context)

#supplier add plant
def add_plant(request):
    # Ensure the user is a supplier
    try:
        supplier = request.user.supplier
    except Supplier.DoesNotExist:
        return redirect('plant_list')  # Or handle appropriately

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

#supplier edit plant 
def edit_plant(request, plant_id):
    # Ensure the user is a supplier
    try:
        supplier = request.user.supplier
    except Supplier.DoesNotExist:
        return redirect('plant_list')  # Or handle appropriately

    plant = get_object_or_404(Plant, id=plant_id, supplier=supplier)
    if request.method == 'POST':
        form = PlantForm(request.POST, request.FILES, instance=plant)
        if form.is_valid():
            form.save()
            return redirect('supplier_dashboard')
    else:
        form = PlantForm(instance=plant)
    return render(request, 'store/edit_plant.html', {'form': form, 'plant': plant})

#supplier delete plant
def delete_plant(request, plant_id):
    # Ensure the user is a supplier
    try:
        supplier = request.user.supplier
    except Supplier.DoesNotExist:
        return redirect('plant_list')  # Or handle appropriately

    plant = get_object_or_404(Plant, id=plant_id, supplier=supplier)
    if request.method == 'POST':
        plant.delete()
        return redirect('supplier_dashboard')
    return render(request, 'store/delete_plant.html', {'plant': plant})

@login_required
def update_customer_details(request):
    try:
        customer = request.user.customer
    except Customer.DoesNotExist:
        customer = None

    if request.method == 'POST':
        form = CustomerUpdateForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('plant_list')  # Redirect to a customer dashboard or some success page
    else:
        form = CustomerUpdateForm(instance=customer)
    return render(request, 'store/update_customer_details.html', {'form': form})

@login_required
def update_supplier_details(request):
    supplier = request.user.supplier
    if request.method == 'POST':
        form = SupplierUpdateForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('supplier_dashboard')  # Redirect to a supplier dashboard or some success page
    else:
        form = SupplierUpdateForm(instance=supplier)
    return render(request, 'store/update_supplier_details.html', {'form': form})


@login_required
def place_order(request):
    try:
        customer = request.user.customer
    except Customer.DoesNotExist:
        return redirect('complete_profile')

    # Check if all required fields in the customer profile are filled
    if not customer.first_name or not customer.last_name or not customer.address:
        messages.error(request, "Please complete your profile before placing an order.")
        return redirect('complete_profile')

    cart = Cart.objects.get(user=request.user)
    cart_items = cart.cartitem_set.all()

    if request.method == "POST":
        for item in cart_items:
            plant = item.plant
            quantity = item.quantity

            if plant.stock >= quantity:
                Order.objects.create(
                    customer=customer,
                    plant=plant,
                    quantity=quantity
                )
                plant.stock -= quantity
                plant.save()
            else:
                messages.error(request, f"Not enough stock available for {plant.name}.")
                return redirect('cart')

        cart.cartitem_set.all().delete()

        messages.success(request, "Order placed successfully!")
        return redirect('order_success')

    return render(request, 'store/place_order.html', {'cart_items': cart_items})





# Order success
def order_success(request):
    return render(request, 'store/order_success.html')

@login_required
def complete_profile(request):
    try:
        customer = request.user.customer
    except Customer.DoesNotExist:
        customer = None

    if request.method == 'POST':
        form = CustomerUpdateForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile completed successfully!")
            return redirect('plant_list')
    else:
        form = CustomerUpdateForm(instance=customer)

    return render(request, 'store/complete_profile.html', {'form': form})
