from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Product, CustomerProfile


# ==========================================
# PRODUCT FORM
# ==========================================

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product

        fields = [
            'name',
            'price',
            'description',
            'category',
            'subcategory',
            'image',
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product name'
            }),

            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product price',
                'step': '0.01'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product description',
                'rows': 5
            }),

            'category': forms.Select(attrs={
                'class': 'form-control'
            }),

            'subcategory': forms.Select(attrs={
                'class': 'form-control'
            }),

            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }


# ==========================================
# USER REGISTRATION FORM
# ==========================================

class RegisterForm(UserCreationForm):

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address',
            'autocomplete': 'email'
        })
    )

    class Meta:
        model = User

        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Choose a username',
                'autocomplete': 'username'
            }),
        }

    def save(self, commit=True):
        user = super().save(commit=False)

        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


# ==========================================
# CUSTOMER PROFILE FORM
# ==========================================

class CustomerProfileForm(forms.ModelForm):

    class Meta:
        model = CustomerProfile

        fields = [
            'phone',
            'address',
            'city',
            'pincode',
        ]

        widgets = {
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number'
            }),

            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full address',
                'rows': 3
            }),

            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your city'
            }),

            'pincode': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your PIN code'
            }),
        }
     
        