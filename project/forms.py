from django import forms
from project.models import Dish, DishPrice, Table, TablePrice, Comment, Stars, Order, Check, CartOfPrivileges, Allergies, LanguageOfCommunication, ExtraInfoUser
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SearchForm(forms.Form):
    q = forms.CharField(label='Search', max_length=100)

class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=254)
  

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')
        exclude = ['username']
        

class DishForm(forms.ModelForm):
    
    class Meta:
        model = Dish
        fields = ['name', 'ingredients', 'gram', 'allergies', 'sort_daytime', 'sort', 'image']
        
        
class TableForm(forms.ModelForm):
    
    class Meta:
        model = Table
        fields = ['name', 'number_of_people', "zone", "sort", 'image']
        
class DishPriceForm(forms.ModelForm):
    
    class Meta:
        model = DishPrice
        fields = ['price', 'date']
        
class TablePriceForm(forms.ModelForm):
    
    class Meta:
        model = TablePrice
        fields = [ 'price', 'date']
        
class CommentForm(forms.Form):
    
    class Meta:
        model = Comment
        fields = ("id_client", 'id_dish','text', 'date', 'image')
        
class StarsForm(forms.Form):
    
    class Meta:
        model = Stars
        fields = ("id_client", 'id_dish','stars', 'date')
        
class CheckForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
    
    class Meta:
        model = Check
        fields = ['id_table']
        

class OrderForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['id_check'].queryset = Check.objects.filter(id_client=user, status="Current")
    
    class Meta:
        model = Order
        fields = ["id_check", "number"]
        
class CartOfPrivilegesForm(forms.ModelForm):
    
    class Meta:
        model = CartOfPrivileges
        fields = ["id_client", "discount"]
                
class AllergiesForm(forms.ModelForm):
    
    class Meta:
        model = Allergies
        fields = ["name", "description"]   
             
class LanguageOfCommunicationForm(forms.ModelForm):
    
    class Meta:
        model = LanguageOfCommunication
        fields = ["language"]      
          
class ExtraInfoUserForm(forms.ModelForm):
    
    class Meta:
        model = ExtraInfoUser
        fields = ["user", "birthday", "allergies", "language_of_communication", "discount"]