from django.conf import settings
from django.db import models
from django import forms

from django.conf import settings
from django.db import models

class Supplier(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=255)  # Changed from forms.CharField
    last_name = models.CharField(max_length=255)   # Changed from forms.CharField
    email = models.EmailField()                    # Changed from forms.EmailField
    address = models.TextField()                   # Changed from forms.CharField(widget=forms.Textarea)
    company_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return self.company_name


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Plant(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='plants')
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='plants/', blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField()

    def __str__(self):
        return self.first_name + " " + self.last_name

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cart of {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.plant.name}"

    def get_total_price(self):
        return self.quantity * self.plant.price

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    plant = models.ForeignKey(Plant, on_delete=models.PROTECT)  # Ensuring plants in orders cannot be deleted
    order_date = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'Order {self.id} by {self.customer}'
