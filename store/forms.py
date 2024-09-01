from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Customer, Supplier
from .models import Plant

# Supplier Sign-Up Form
class SupplierSignUpForm(UserCreationForm):
    company_name = forms.CharField(max_length=255)
    contact_number = forms.CharField(max_length=15)
    address = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'company_name', 'contact_number', 'address']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            Supplier.objects.create(
                user=user,
                company_name=self.cleaned_data['company_name'],
                contact_number=self.cleaned_data['contact_number'],
                address=self.cleaned_data['address']
            )
        return user

# Customer Sign-Up Form
class CustomerSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    email = forms.EmailField()
    address = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'address']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Customer.objects.create(
                user=user,
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                email=self.cleaned_data['email'],
                address=self.cleaned_data['address']
            )
        return user

class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = ['name', 'description', 'price', 'image', 'stock', 'category']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class CustomerUpdateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'address']

class SupplierUpdateForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['company_name', 'contact_number', 'address']