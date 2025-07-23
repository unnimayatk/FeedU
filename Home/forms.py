from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserAddForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username", "password1", "password2"]

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'id': 'username', 'placeholder': 'User Name'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'first_name', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'last_name', 'placeholder': 'Last Name'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'id': 'email', 'placeholder': 'Email Id'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password1', 'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password2', 'placeholder': 'Confirm Password'}),
        }



from .models import FoodMenuItem

class FoodMenuItemForm(forms.ModelForm):
    class Meta:
        model = FoodMenuItem
        fields = ['name',"category", 'image', 'description', 'rate', 'discount_rate']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Item Name'}),
            "category":forms.Select(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'rate': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Rate'}),
            'discount_rate': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Discount Rate'}),
            'offer': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
