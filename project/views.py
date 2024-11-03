from django.shortcuts import render, reverse, redirect
from django.urls import reverse_lazy
from .models import Dish, DishPrice, Table, TablePrice, Comment, Stars, Order, Check, UserDate
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.views import LogoutView
#from project.forms import
from django.contrib.auth.mixins import LoginRequiredMixin
#from project.mixins import 
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from .forms import LoginForm, SignupForm
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


# Create your views here.
