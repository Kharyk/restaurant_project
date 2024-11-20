from django.shortcuts import render, reverse, redirect
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from project.models import Dish, DishPrice, Table, TablePrice, Comment, Stars, Order, Check
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
from django.http import JsonResponse
from django.template.loader import render_to_string


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
                return redirect('dish-list')  
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

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']

            username = email.split('@')[0]  # Use the part before the @ in the email as username
            if User.objects.filter(username=username).exists():
                form.add_error('email', 'The generated username is already taken. Please choose a different email address.')
                return render(request, self.template_name, {'form': form})

            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dish-list')

        print(form.errors)
        return render(request, self.template_name, {'form': form})

class HomepageView(TemplateView):
    template_name = 'home.html'

class LearnMoreView(TemplateView):
    template_name = 'learn_more.html'
    
class AboutUsView(TemplateView):
    template_name = 'about_us.html'

class ContactView(LoginRequiredMixin, TemplateView):
    template_name = 'contact.html'
    




class DishListView(ListView):
    model = Dish
    template_name = 'dish/dish_list.html'
    context_object_name = 'dishes'
    paginate_by = 8
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dishes = context['dishes']

        latest_prices = {}
        for dish in dishes:
            latest_price = DishPrice.objects.filter(dish=dish).order_by('-date').first()
            latest_prices[dish.id] = latest_price

        context['latest_prices'] = latest_prices
        return context

    def get(self, request): 
        super().get(request) 
        if request.headers.get('x-requested-with') == 'XMLHttpRequest': 
            return render (request, 'dish/list.html', context=self.get_context_data()) 
        return render(request, self.template_name, context=self.get_context_data())

class DishCreateView(CreateView):
    model = Dish
    form_class = DishForm
    template_name = 'dish/dish_form.html'
    success_url = reverse_lazy('dish-list')
    

class DishDetailView(DetailView):
    model = Dish
    template_name = 'dish/dish_detail.html' 
    context_object_name = 'dish'  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dish = self.object  
        latest_price = DishPrice.objects.filter(dish=dish).order_by('-date').first()
        context['latest_price'] = latest_price  
        return context

class DishUpdateView(UpdateView):
    model = Dish
    form_class = DishForm
    template_name = 'dish/dish_form.html'
    success_url = reverse_lazy('dish-list')   

class DishDeleteView(DeleteView):
    model = Dish
    template_name = 'dish/dish_confirm_delete.html'
    success_url = reverse_lazy('dish-list')
    
    


    
class TableCreateView(LoginRequiredMixin, CreateView):
    
    model = Table
    template_name = "table/table_form.html"
    form_class = TableForm
    success_url = reverse_lazy("table-list")
    
class TableListView(ListView):
    
    model = Table
    template_name = "table/table_list.html"
    context_object_name = "tables"
    paginate_by = 4
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tables = context['tables']

        latest_prices = {}
        for table in tables:
            latest_price = TablePrice.objects.filter(table=table).order_by('-date').first()
            latest_prices[table.id] = latest_price

        context['latest_prices'] = latest_prices
        return context
    
    def get(self, request): 
        super().get(request) 
        if request.headers.get('x-requested-with') == 'XMLHttpRequest': 
            return render (request, 'table/list.html', context=self.get_context_data()) 
        return render(request, self.template_name, context=self.get_context_data())
    
class TableDetailView(DetailView):
    
    model = Table
    template_name = "table/table_detail.html"
    context_object_name = 'table'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        table = self.object  
        latest_price = TablePrice.objects.filter(table=table).order_by('-date').first()
        context['latest_price'] = latest_price  
        return context
    
class TableUpdateView(LoginRequiredMixin, UpdateView):
    model = Table
    template_name = "table/table_form.html"
    form_class = TableForm

    def get_success_url(self):
        return reverse('table-detail', kwargs={'pk': self.object.pk})
    
class TableDeleteView(LoginRequiredMixin, DeleteView):
    
    model = Table
    template_name = "table/table_confirm_delete.html"
    success_url = reverse_lazy("table-list")
    
    

class DishPriceCreateView(LoginRequiredMixin, CreateView):
    model = DishPrice
    template_name = "dish_price/dish_price_form.html"
    form_class = DishPriceForm

    def get_success_url(self):
        return reverse_lazy("dish-detail", kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dish'] = Dish.objects.get(pk=self.kwargs['pk'])  
        return context

    def form_valid(self, form):
        form.instance.dish_id = self.kwargs['pk']  
        return super().form_valid(form)
    
# class DishPriceListView(ListView):
    
#     model = DishPrice
#     tamplate_name = "dish_price/dish_price_list.html"
#     context_object_name = "dish_prices"
    
class DishPriceDetailView(DetailView):
    
    model = DishPrice
    template_name = "dish_price/dish_price_dateil.html"
    context_object_name = "dish_price"
    
# class DishPriceUpdateView(LoginRequiredMixin, UpdateView):
    
#     model = DishPrice
#     template_name = "dish_price/dish_price_update.html"    
#     form_class = DishPriceForm
#     success_url = reverse_lazy("dish-price-detail")
    
# class DishPriceDeleteView(LoginRequiredMixin, DeleteView):
    
#     model = DishPrice
#     template_name = "dish_price/dish_price_confirm_delete.html"
#     success_url = reverse_lazy("dish-price-list")

    
class TablePriceCreateView(LoginRequiredMixin, CreateView):
    
    model = TablePrice
    template_name = "table_price/table_price_form.html"
    form_class = TablePriceForm
    
    def get_success_url(self):
        return reverse_lazy("table-detail", kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table'] = Table.objects.get(pk=self.kwargs['pk'])  
        return context

    def form_valid(self, form):
        form.instance.table_id = self.kwargs['pk']  
        return super().form_valid(form)
    
# class TablePriceListView(ListView):
    
#     model = TablePrice
#     template_name = "table_price/table_price_list.html"
#     context_object_name = "table_prices"
    
class TablePriceDetailView(DetailView):
    
    model = TablePrice
    template_name = "table_price/table_price_detail.html"
    context_object_name = "table_price"
    
# class TablePriceUpdateView(LoginRequiredMixin, UpdateView):
    
#     model = TablePrice
#     template_name = "table_price/table_price_update.html"
#     form_class = TablePriceForm
#     success_url = reverse_lazy("table-price-detail")
    
# class TablePriceDeleteView(LoginRequiredMixin, DeleteView):
    
#     model = TablePrice
#     template_name = "table_price/table_price_confirm_delete.html"
#     success_url = reverse_lazy("table-price-list")
    


class CommentCreateView(LoginRequiredMixin, CreateView):
    
    model = Comment
    template_name = "comment/comment_form.html"
    form_class = CommentForm
    success_url = reverse_lazy("dish-detail")
    
class CommentUpdateView(LoginRequiredMixin, UpdateView):
    
    model = Comment
    template_name = "comment/comment_update.html"
    form_class = CommentForm
    success_url = reverse_lazy("dish-detail")
    
class CommentDeleteView(LoginRequiredMixin, DeleteView):
    
    model = Comment
    template_name = "comment/comment_confirm_delete.html"
    success_url = reverse_lazy("dish-detail")
    
    
    
class StarsCreateView(LoginRequiredMixin, CreateView):
    
    model = Stars
    template_name = "stars/stars_form.html"
    form_class = StarsForm
    success_url = reverse_lazy("dish-detail")
    
class StarsUpdateView(LoginRequiredMixin, UpdateView):
    
    model = Stars
    template_name = "stars/stars_update.html"
    form_class = StarsForm
    success_url = reverse_lazy("dish-detail")
    
class StarsDeleteView(LoginRequiredMixin, DeleteView):
    
    model = Stars
    template_name = "stars/stars_confirm_delete.html"
    success_url = reverse_lazy("dish-detail")
    
    
    
class CheckCreateView(LoginRequiredMixin, CreateView):
    
    model = Check
    template_name = "check/check_form.html"
    form_class = CheckForm
    
    def form_valid(self, form):
        self.object = form.save()  
        self.success_url = reverse_lazy("check-detail", kwargs={'pk': self.object.pk})  
        return super().form_valid(form)
    
class CheckListView(LoginRequiredMixin, ListView):
    
    model = Check
    template_name = "check/check_list.html"
    context_object_name = "checks"
    
class CheckDetailView(LoginRequiredMixin, DetailView):
    
    model = Check
    template_name = "check/check_detail.html"
    form_class = CheckForm
    success_url = reverse_lazy("check-detail")
    
class CheckUpdateView(LoginRequiredMixin, UpdateView):
    
    model = Check
    template_name = "check/check_update.html"
    form_class = CheckForm
    success_url = reverse_lazy("check-detail")
    
class CheckDeleteView(LoginRequiredMixin, DeleteView):
    
    model = Check
    template_name = "check/check_confirm_delete.html"
    success_url = reverse_lazy("dish-list")
    
    
    
    
class OrderCreateView(LoginRequiredMixin, CreateView):
    
    model = Order
    template_name = "order/order_form.html"
    form_class = OrderForm
    
    def form_valid(self, form):
        self.object = form.save()  
        self.success_url = reverse_lazy("order-detail", kwargs={'pk': self.object.pk})  
        return super().form_valid(form)
   
    
    # def form_valid(self, form):
    #     form.instance.id_client = self.request.user
    #     return super().form_valid(form)

    # def post(self, request, *args, **kwargs):
    #     if request.method == 'POST':
    #         form = self.form_class(request.POST)
    #         if form.is_valid():
    #             form.instance.id_client = self.request.user
    #             form.save()
    #             return redirect(self.success_url)
    #         else:
    #             return render(request, self.template_name, {'form': form})
    #     else:
    #         form = self.form_class()
    #         return render(request, self.template_name, {'form': form})

    # def get(self, request, *args, **kwargs):
    #     form = self.form_class()
    #     return render(request, self.template_name, {'form': form})

    
class OrderListView(LoginRequiredMixin, ListView):
    
    model = Order
    template_name = "order/order_list.html"
    context_object_name = "orders"
    
class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = "order/order_detail.html"
    form_class = OrderForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.object
        
        # Get the dish prices
        dish_prices = []
        for dish in order.id_dishes.all():
            latest_price = DishPrice.objects.filter(dish=dish).order_by('-date').first()
            if latest_price:
                dish_prices.append({
                    'dish': dish,
                    'price': latest_price.price,
                    'quantity': order.number,  # Assuming order.number is the quantity for all dishes
                    'total_price': latest_price.price * order.number
                })
        
        context['dish_prices'] = dish_prices
        return context
    
    
class OrderUpdateView(LoginRequiredMixin, UpdateView):
    
    model = Order
    template_name = "order/order_update.html"
    form_class = OrderForm
    
    def get_success_url(self):
        return reverse('order-detail', kwargs={'pk': self.object.pk})
    
class OrderDeleteView(LoginRequiredMixin, DeleteView):
    
    model = Order
    template_name = "order/order_confirm_delete.html"
    success_url = reverse_lazy("dish-list")
    
    
    
    

# Create your views here.