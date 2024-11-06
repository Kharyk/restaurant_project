from django.shortcuts import render, reverse, redirect
from django.urls import reverse_lazy
from .models import Dish, DishPrice, Table, TablePrice, Comment, Stars, Order, Check, UserDate
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.views import LogoutView
from project.forms import DishForm, TableForm, DishPriceForm, TablePriceForm, CommentForm, StarsForm, CheckForm, OrderForm
from django.contrib.auth.mixins import LoginRequiredMixin
#from project.mixins import 
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from .forms import LoginForm, SignupForm, SearchForm
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.decorators import method_decorator

class SearchResultsView(View):
    @method_decorator(login_required)
    def get(self, request):
        query = request.GET.get('q')
        if query:
            dish = Dish.objects.filter(
                Q(name__icontains=query) | 
                Q(ingredients__icontains=query) | 
                Q(sort__icontains=query)
            )
            table = Table.objects.filter(
                Q(name__icontains=query) | 
                Q(zone__icontains=query) | 
                Q(sort__icontains=query)
            )
        else:
            tasks = Dish.objects.none()
            projects = Table.objects.none()
        return render(request, 'search_results.html', {'dish': dishs, 'table': tables, 'query': query})

class LoginView(View):
    template_name = 'login.html'
    form_class = LoginForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('')  ######### do not forget to write file.html
            else:
                form.add_error(None, 'Invalid username or password')
        return render(request, self.template_name, {'form': form})


class CustomLogoutView(LogoutView):

    def get(self, request):
        return super().get(request)

class SignupView(View):
    template_name = 'signup.html'
    form_class = SignupForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def register_user(request):
        if request.method == "POST":
            form = SignUpForm(request.POST)
            if form.is_valid():
                user = form.save()  
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                age = form.cleaned_data.get('age')

                user_data = UserData.objects.create(user=user, age=age)
                user_data.save()

                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('')   ######### do not forget to write file.html

        else:
            form = SignUpForm()
        
        return render(request, 'project/signup.html', {'form': form}) ######### do not forget to write file.html

class HomepageView(TemplateView):
    template_name = 'home.html'

class LearnMoreView(TemplateView):
    template_name = 'learn_more.html'

class ContactView(LoginRequiredMixin, TemplateView):
    template_name = 'contact.html'
    
    
    
    
class DishCreateView(CreateView):
    
    model = models.Dish
    template_name =  "dish/dish_form.html"
    form_class = DishForm
    success_url = reverse_lazy("dish-list")
    
class DishListView(ListView):
    
    model = models.Dish
    template_name = "dish/dish_list.html"
    context_object_name = "dishes"
    
class DishDetailView(DetailView):
    model = models.Dish
    template_name = "dish/dish_detail.html"
    context_object_name = 'dish'
    
class DishUpdateView(UpdateView):
    
    model = models.Dish
    template_name = "dish/dish_update.html"
    form_class = DishForm
    success_url = reverse_lazy("dish-detail")
    
class DishDeleteView(DeleteView):
    
    model = models.Dish
    template_name = "dish/dish_confirm_delete.html"
    success_url = reverse_lazy("dish-list")
    
    
    
    
class TableCreateView(CreateView):
    
    model = models.Table
    template_name = "table/table_form.html"
    form_class = TableForm
    success_url = reverse_lazy("table-list")
    
class TableListView(ListView):
    
    model = models.Table
    template_name = "table/table_list.html"
    context_object_name = "tables"
    
class TableDetailView(DetailView):
    
    model = models.Table
    template_name = "table/table_detail.html"
    context_object_name = 'table'
    
class TableUpdateView(UpdateView):
    
    model = models.Table
    template_name = "table/table_update.html"
    form_class = TableForm
    success_url = reverse_lazy("table-detail")
    
class TableDeleteView(DeleteView):
    
    model = models.Table
    template_name = "table/table_confirm_delete.html"
    success_url = reverse_lazy("table-list")
    
    

class DishPriceCreateView(CreateView):
    
    model = models.DishPrice
    template_name = "dish_price/dish_price_form.html"
    form_class = DishPriceForm
    success_url = reverse_lazy("dish-price-list")
    
class DishPriceListView(ListView):
    
    model = models.DishPrice
    tamplate_name = "dish_price/dish_price_list.html"
    context_object_name = "dish_prices"
    
class DishPriceDetailView(DetailView):
    
    model = models.DishPrice
    template_name = "dish_price/dish_price_dateil.html"
    context_object_name = "dish_price"
    
class DishPriceUpdateView(UpdateView):
    
    model = models.DishPrice
    template_name = "dish_price/dish_price_update.html"    
    form_class = DishPriceForm
    success_url = reverse_lazy("dish-price-detail")
    
class DishPriceDeleteView(DeleteView):
    
    model = models.DishPrice
    template_name = "dish_price/dish_price_confirm_delete.html"
    success_url = reverse_lazy("dish-price-list")

    


class TablePriceCreateView(CreateView):
    
    model = models.TablePrice
    template_name = "table_price/table_price_form.html"
    form_class = TablePriceForm
    success_url = reverse_lazy("table-price-list")
    
class TablePriceListView(ListView):
    
    model = models.TablePrice
    template_name = "table_price/table_price_list.html"
    context_object_name = "table_prices"
    
class TablePriceDetailView(DetailView):
    
    model = models.TablePrice
    template_name = "table_price/table_price_detail.html"
    context_object_name = "table_price"
    
class TablePriceUpdateView(UpdateView):
    
    model = models.TablePrice
    template_name = "table_price/table_price_update.html"
    form_class = TablePriceForm
    success_url = reverse_lazy("table-price-detail")
    
class TablePriceDeleteView(DeleteView):
    
    model = models.tablePrice
    template_name = "table_price/table_price_confirm_delete.html"
    success_url = reverse_lazy("table-price-list")
    


class CommentCreateView(CreateView):
    
    model = models.Comment
    template_name = "comment/comment_form.html"
    form_class = CommentForm
    success_url = reverse_lazy("dish-detail")
    
class CommentUpdateView(UpdateView):
    
    model - models.Comment
    template_name = "comment/comment_update.html"
    form_class = CommentForm
    success_url = reverse_lazy("dish-detail")
    
class CommentDeleteView(DeleteView):
    
    model = models.Comment
    template_name = "comment/comment_confirm_delete.html"
    success_url = reverse_lazy("dish-detail")
    
    
    
class StarsCreateView(CreateView):
    
    model = models.Stars
    template_name = "stars/stars_form.html"
    form_class = StarsForm
    success_url = reverse_lazy("dish-detail")
    
class StarsUpdateView(UpdateView):
    
    model = models.Stars
    template_name = "stars/stars_update.html"
    form_class = StarsForm
    success_url = reverse_lazy("dish-detail")
    
class StarsDeleteView(DeleteView):
    
    model = models.Stars
    template_name = "stars/stars_confirm_delete.html"
    success_url = reverse_lazy("dish-detail")
    
    
    
class CheckCreateView(CreateView):
    
    model = models.Check
    template_name = "check/check_form.html"
    form_class = CheckForm
    success_url = reverse_lazy("dish-list")
    
class CheckListView(ListView):
    
    model = models.Check
    template_name = "check/check_list.html"
    context_object_name = "checks"
    
class CheckDetailView(DetailView):
    
    model = models.Check
    template_name = "check/check_detail.html"
    form_class = CheckForm
    success_url = reverse_lazy("check-detail")
    
class CheckUpdateView(UpdateView):
    
    model = models.Check
    template_name = "check/check_update.html"
    form_class = CheckForm
    success_url = reverse_lazy("check-detail")
    
class CheckDeleteView(DeleteView):
    
    model = models.Check
    template_name = "check/check_confirm_delete.html"
    success_url = reverse_lazy("dish-list")
    
    
    
    
class OrderCreateView(CreateView):
    
    model = models.Order
    template_name = "order/order_form.html"
    form_class = OrderForm
    success_url = reverse_lazy("dish-list")
    
class OrderListView(listView):
    
    model = models.Order
    template_name = "order/order_list.html"
    context_object_name = "orders"
    
class OrderDetailView(DetailView):
    
    model = models.Order
    template_name = "order/order_detail.html"
    form_class = OrderForm
    success_url = reverse_lazy("order-detail")
    
class OrderUpdateView(UpdateView):
    
    model = models.Order
    template_name = "order/order_update.html"
    form_class = OrderForm
    success_url = reverse_lazy("order-detail")
    
class OrderDeleteView(DleteView):
    
    model = models.Order
    template_name = "order/order_confirm_delete.html"
    success_url = reverse_lazy("dish-list")
    
    
    
    

# Create your views here.
