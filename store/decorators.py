# store/decorators.py

from django.shortcuts import redirect
from django.contrib import messages
from .models import Supplier
def supplier_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "You need to be logged in as a supplier to access this page.")
            return redirect('supplier_login')
        try:
            request.user.supplier
        except Supplier.DoesNotExist:
            messages.error(request, "You need to be a supplier to access this page.")
            return redirect('plant_list')  # Or redirect to signup
        return view_func(request, *args, **kwargs)
    return wrapper
