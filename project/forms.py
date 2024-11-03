from django import forms
from system.models import Dish, DishPrice, Table, TablePrice, Comment, Stars, Order, Check
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SearchForm(forms.Form):
    q = forms.CharField(label='Search', max_length=100)

class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=254)
    age = forms.IntegerField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'age', 'password1', 'password2')
        exclude = ['username']