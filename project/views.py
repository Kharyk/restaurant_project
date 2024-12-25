from django.shortcuts import render, reverse, redirect
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from project.models import Dish, DishPrice, Table, TablePrice, Comment, Stars, Order, Check, CartOfPrivileges, Allergies, LanguageOfCommunication, ExtraInfoUser
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.views import LogoutView
from project.forms import DishForm, TableForm, DishPriceForm, TablePriceForm, CommentForm, StarsForm, CheckForm, OrderForm, ExtraInfoUserForm, LanguageOfCommunicationForm, AllergiesForm, CartOfPrivilegesForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from project.mixin import StaffRequiredMixin
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
from django.db.models import OuterRef, Subquery





from django.db.models import Q
from .models import Dish

def dish_search(request):
    queryset = Dish.objects.all()
    
    query = request.GET.get('q', '')
    daytime = request.GET.get('daytime', '')
    category = request.GET.get('category', '')
    
    if query:
        queryset = queryset.filter(
            Q(name__icontains=query) | 
            Q(ingredients__icontains=query)
        )
    
    if daytime:
        queryset = queryset.filter(sort_daytime=daytime)
    
    if category:
        queryset = queryset.filter(sort=category)
    
    context = {
        'dishes': queryset,
        'query': query,
        'daytime': daytime,
        'category': category,
        'daytime_choices': Dish.SORTDT,
        'category_choices': Dish.SORT
    }
    
    return render(request, 'search_result.html', context)
    

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
    template_name = "home.html"
    success_url = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('home')
        

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

class ContactView(TemplateView):
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
        self.object = form.save(commit=False)
        self.object.id_client = self.request.user
        self.object.save()
        self.success_url = reverse_lazy("check-detail", kwargs={'pk': self.object.pk})
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    

class CheckCurrentListView(ListView):
    model = Check
    template_name = "check/check_list.html"
    context_object_name = "checks"
    
    def get_queryset(self):
        return self.request.user.check_set.filter(
            Q(status='Current')
        )
    
class CheckInProcessListView(ListView):
    model = Check
    template_name = "check/check_list.html"
    context_object_name = "checks"
    
    def get_queryset(self):
        return self.request.user.check_set.filter(
            Q(status='Want to pay') 
        )
        
class CheckHistoryListView(ListView):
    model = Check
    template_name = "check/check_list.html"
    context_object_name = "checks"
    
    def get_queryset(self):
        return self.request.user.check_set.filter(
            Q(status='Paid')
        )
    


'''
def check_list_view(request):
    if request.user.is_authenticated:
        unpaid_checks_count = Check.objects.filter(id_client=request.user, status="In process").count()
        show_create_button = unpaid_checks_count < 5
        checks = Check.objects.filter(id_client=request.user, status="In process")
    else:
        unpaid_checks_count = 0
        show_create_button = False
        checks = []

    return render(request, 'check/list.html', {
        'checks': checks,
        'unpaid_checks_count': unpaid_checks_count,
        'show_create_button': show_create_button,
    })
'''


class CheckDetailView(LoginRequiredMixin, DetailView):
    model = Check
    template_name = "check/check_detail.html"
    context_object_name = "check"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        check = self.object  # The current Check instance

        # Initialize orders and total price
        orders = []
        total_price = 0

        # Fetch related orders and calculate prices
        for order in check.orders.all():
            for dish in order.id_dishes.all():
                latest_price = DishPrice.objects.filter(dish=dish, date__lte=check.date).order_by('-date').first()
                price = latest_price.price if latest_price else 0
                quantity = order.number
                total = price * quantity
                orders.append({
                    'dish': dish.name,
                    'quantity': quantity,
                    'price': price,
                    'total': total,
                })
                total_price += total

        # Add table price if applicable
        latest_table_price = TablePrice.objects.filter(table=check.id_table, date__lte=check.date).order_by('-date').first()
        if latest_table_price:
            total_price += latest_table_price.price
            context["table_price"] = latest_table_price.price
        else:
            context["table_price"] = 0

        # Add calculated data to the context
        context["orders"] = orders
        context["total_price"] = total_price
        return context


    


class CheckUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Check
    template_name = 'check/check_update.html'
    fields = ['id_client', 'id_table', 'status']

    def test_func(self):
        return self.request.user.is_superuser

    def get_success_url(self):
        return reverse_lazy('check-detail', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        check = self.get_object()
        context.update({
            'users': User.objects.all(),
            'tables': Table.objects.all(),
            'dishes': Dish.objects.all(),
            'latest_price': check.id_table.tableprice_set.filter(date__lte=check.date).order_by('-date').first(),
            'latest_prices': self.get_latest_prices(check),  # Pass the check object to get_latest_prices
        })
        return context

    def get_latest_prices(self, check):
        latest_prices = {}
        dishes = Dish.objects.all()
        for dish in dishes:
            latest_price = DishPrice.objects.filter(dish=dish, date__lte=check.date).order_by('-date').first()
            latest_prices[dish.id] = latest_price.price if latest_price else 0.00
        return latest_prices



    # def get_latest_prices(self):
    #     latest_prices = {}
    #     # Get the current check object
    #     check = self.object
    #     # Fetch all dishes
    #     dishes = Dish.objects.all()
        
    #     for dish in dishes:
    #         # Get the latest price for each dish based on the check date
    #         latest_price = DishPrice.objects.filter(dish=dish, date__lte=check.date).order_by('-date').first()
    #         latest_prices[dish.id] = latest_price.price if latest_price else 0.00
        
    #     return latest_prices

    def form_valid(self, form):
        # Handle order updates/additions here
        # You'll need custom logic to update or create new orders
        # Example: You can access the orders from the form data and update them accordingly
        # This is a placeholder for your logic
        orders_data = self.request.POST.getlist('order_data')  # Example of how you might get order data
        # Process orders_data to update or create orders

        return super().form_valid(form)
    
class CheckDeleteView(LoginRequiredMixin, DeleteView):
    
    model = Check
    template_name = "check/check_confirm_delete.html"
    success_url = reverse_lazy("dish-list")
    
    

class CheckWaiterListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = Check
    template_name = "waiter/check_list.html"
    context_object_name = "checks"
    
    def test_func(self):
        return self.request.user.is_staff
    
    def get_queryset(self):
        # Filter to only include checks with status 'wtp'
        return Check.objects.filter(status='Want to pay')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sorts'] = [
            ("Paid", "Paid"),
            ("Want to pay", "Want to pay"),
            ("Current", "Current")
        ]
        return context
    
    
def check_waiter_list_view(request):
    if not request.user.is_staff:
        return redirect('login')
    
    context = {
        'check': Check.objects,
        # other context variables
    }
    
    return render(request, "waiter/check_list.html", context)
    
def change_status_pay(request, check_id):
    check = get_object_or_404(Check, id=check_id)
    
    if check.status != "Want to pay":
        check.status = "Want to pay"
        check.save()
    
    return JsonResponse({'status': check.status})   

def change_status_done(request, check_id):
    check = get_object_or_404(Check, id=check_id)
    
    check.status = "Paid"
    check.save()
    
    return JsonResponse({'status': check.status})



class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'order/order_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        dish = get_object_or_404(Dish, pk=self.kwargs['pk'])
        
        form.instance.id_client = self.request.user
        
        self.object = form.save(commit=False)
        
        self.object.save() 
        self.object.id_dishes.add(dish)  
        
        self.success_url = reverse_lazy("dish-list")
        
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dish'] = get_object_or_404(Dish, pk=self.kwargs['pk'])
        return context

    

    
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
        
        dish_prices = []
        for dish in order.id_dishes.all():
            latest_price = DishPrice.objects.filter(dish=dish).order_by('-date').first()
            if latest_price:
                dish_prices.append({
                    'dish': dish,
                    'price': latest_price.price,
                    'quantity': order.number, 
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
    
    
    
class CartOfPrivilegesListView(LoginRequiredMixin, ListView):
    model = CartOfPrivileges
    template_name = 'cart_of_privileges/cart_of_privileges_list.html'
    context_object_name = 'privileges'

    def get_queryset(self):
        return CartOfPrivileges.objects.filter(id_client=self.request.user)

class CartOfPrivilegesDetailView(LoginRequiredMixin, DetailView):
    model = CartOfPrivileges
    form_class = CartOfPrivilegesForm
    template_name = 'cart_of_privileges/cart_of_privileges_detail.html'


class CartOfPrivilegesCreateView(LoginRequiredMixin, CreateView):
    model = CartOfPrivileges
    template_name = 'cart_of_privileges/cart_of_privileges_form.html'
    form_class = CartOfPrivilegesForm
    
    def dispatch(self, request, *args, **kwargs):
        if CartOfPrivileges.objects.filter(id_client=request.user).exists():
            return redirect('cart-privileges-list')
        return super().dispatch(request, *args, **kwargs)
    
    
    def form_valid(self, form):
        form.instance.id_client = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('cart-privileges-list')

    
class CartOfPrivilegesUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CartOfPrivileges
    template_name = 'cart_of_privileges/cart_of_privileges_form.html'
    form_class = CartOfPrivilegesForm


    def test_func(self):
        privilege = self.get_object()
        return self.request.user == privilege.id_client

    def get_success_url(self):
        return reverse_lazy('cart-privileges-detail', kwargs={'pk': self.object.pk})

class CartOfPrivilegesDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = CartOfPrivileges
    template_name = 'cart_of_privileges/cart_of_privileges_confirm_delete.html'
    success_url = reverse_lazy('cart-privileges-list')

    def check_end_date(self):
        if self.get_object().end_date < datetime.now():
            return False
        return True
        
    
    def test_func(self):
        privilege = self.get_object()
        return self.request.user == privilege.id_client



class AllergiesListView(LoginRequiredMixin, ListView):
    model = Allergies
    template_name = 'allergies/allergies_list.html'
    context_object_name = 'allergies'

# class AllergiesDetailView(LoginRequiredMixin, DetailView):
#     model = Allergies
#     template_name = 'allergies_detail.html'

class AllergiesCreateView(LoginRequiredMixin, CreateView):
    model = Allergies
    template_name = 'allergies/allergies_form.html'
    form_class = AllergiesForm
    success_url = reverse_lazy('allergies-list')

class AllergiesDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Allergies
    template_name = 'allergies/allergie_confirm_delete.html'
    success_url = reverse_lazy('allergies-list')
    
    def test_func(self):
        return self.request.user.is_authenticated  



class LanguageOfCommunicationListView(LoginRequiredMixin, ListView):
    model = LanguageOfCommunication
    template_name = 'language/language_list.html'
    context_object_name = 'languages'
    
# class LanguageOfCommunicationDetailView(LoginRequiredMixin, DetailView):
#     model = LanguageOfCommunication
#     template_name = 'language_detail.html'

class LanguageOfCommunicationCreateView(LoginRequiredMixin, CreateView):
    model = LanguageOfCommunication
    template_name = 'language/languages_form.html'
    form_class = LanguageOfCommunicationForm
    success_url = reverse_lazy('language-list')

class LanguageOfCommunicationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = LanguageOfCommunication
    template_name = 'language/language_confirm_delete.html'
    success_url = reverse_lazy('language-list')
    
    def test_func(self):
       return self.request.user.is_authenticated  
    
    
    
class ExtraInfoUserCreateView(LoginRequiredMixin, CreateView):
    model = ExtraInfoUser
    template_name = 'extra_info_user/extra_info_user_form.html'
    form_class = ExtraInfoUserForm
    success_url = reverse_lazy('dish-list')

class ExtraInfoUserDetailView(LoginRequiredMixin, DetailView):  
    model = ExtraInfoUser
    form_class = ExtraInfoUserForm
    template_name = 'extra_info_user/extra_info_user_detail.html'

    def get_object(self, queryset=None):
        return ExtraInfoUser.objects.get(user=self.request.user)

class ExtraInfoUserUpdateView(LoginRequiredMixin, UpdateView):
    model = ExtraInfoUser
    form_class = ExtraInfoUserForm
    template_name = 'extra_info_user/extra_info_user_form.html'

    def get_object(self, queryset=None):
        extra_info, created = ExtraInfoUser.objects.get_or_create(user=self.request.user)
        return extra_info

    def get_success_url(self):
        return reverse_lazy('extra-info-detail')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class ExtraInfoUserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ExtraInfoUser
    template_name = 'extra_info_user/extra_info_user_delete.html'
    success_url = reverse_lazy('dish-list')

# Create your views here.