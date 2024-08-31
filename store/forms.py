from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Supplier
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Customer
from .models import Plant

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
            supplier = Supplier.objects.create(
                user=user,
                company_name=self.cleaned_data['company_name'],
                contact_number=self.cleaned_data['contact_number'],
                address=self.cleaned_data['address']
            )
        return user
    
class CustomerSignUpForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'address', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError("Passwords do not match")

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['email'],  # Using email as username
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password1']
        )
        customer = Customer.objects.create(
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