"""
URL configuration for restaurant project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import (
    SearchResultsView,
    LoginView,
    CustomLogoutView,
    SignupView,
    HomepageView,
    LearnMoreView,
    ContactView,
    DishCreateView,
    DishListView,
    DishDetailView,
    DishUpdateView,
    DishDeleteView,
    TableCreateView,
    TableListView,
    TableDetailView,
    TableUpdateView,
    TableDeleteView,
    DishPriceCreateView,
    DishPriceListView,
    DishPriceDetailView,
    DishPriceUpdateView,
    DishPriceDeleteView,
    TablePriceCreateView,
    TablePriceListView,
    TablePriceDetailView,
    TablePriceUpdateView,
    TablePriceDeleteView,
    CommentCreateView,
    CommentUpdateView,
    CommentDeleteView,
    StarsCreateView,
    StarsUpdateView,
    StarsDeleteView,
    CheckCreateView,
    CheckListView,
    CheckDetailView,
    CheckUpdateView,
    CheckDeleteView,
    OrderCreateView,
    OrderListView,
    OrderDetailView,
    OrderUpdateView,
    OrderDeleteView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', HomepageView.as_view(), name='home'),
    path('learn-more/', LearnMoreView.as_view(), name='learn-more'),
    path('contact/', ContactView.as_view(), name='contact'),
    
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),

    path('search/', SearchResultsView.as_view(), name='search-results'),

    # Dish URLs
    path('dishes/', DishListView.as_view(), name='dish-list'),
    path('dishes/create/', DishCreateView.as_view(), name='dish-create'),
    path('dishes/<int:pk>/', DishDetailView.as_view(), name='dish-detail'),
    path('dishes/<int:pk>/update/', DishUpdateView.as_view(), name='dish-update'),
    path('dishes/<int:pk>/delete/', DishDeleteView.as_view(), name='dish-delete'),

    # Table URLs
    path('tables/', TableListView.as_view(), name='table-list'),
    path('tables/create/', TableCreateView.as_view(), name='table-create'),
    path('tables/<int:pk>/', TableDetailView.as_view(), name='table-detail'),
    path('tables/<int:pk>/update/', TableUpdateView.as_view(), name='table-update'),
    path('tables/<int:pk>/delete/', TableDeleteView.as_view(), name='table-delete'),

    # Dish Price URLs
    path('dish-prices/', DishPriceListView.as_view(), name='dish-price-list'),
    path('dish-prices/create/', DishPriceCreateView.as_view(), name='dish-price-create'),
    path('dish-prices/<int:pk>/', DishPriceDetailView.as_view(), name='dish-price-detail'),
    path('dish-prices/<int:pk>/update/', DishPriceUpdateView.as_view(), name='dish-price-update'),
    path('dish-prices/<int:pk>/delete/', DishPriceDeleteView.as_view(), name='dish-price-delete'),

    # Table Price URLs
    path('table-prices/', TablePriceListView.as_view(), name='table-price-list'),
    path('table-prices/create/', TablePriceCreateView.as_view(), name='table-price-create'),
    path('table-prices/<int:pk>/', TablePriceDetailView.as_view(), name='table-price-detail'),
    path('table-prices/<int:pk>/update/', TablePriceUpdateView.as_view(), name='table-price-update'),
    path('table-prices/<int:pk>/delete/', TablePriceDeleteView.as_view(), name='table-price-delete'),

    # Comment URLs
    path('comments/create/', CommentCreateView.as_view(), name='comment-create'),
    path('comments/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),
    path('comments/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),

    # Stars URLs
    path('stars/create/', StarsCreateView.as_view(), name='stars-create'),
    path('stars/<int:pk>/update/', StarsUpdateView.as_view(), name='stars-update'),
    path('stars/<int:pk>/delete/', StarsDeleteView.as_view(), name='stars-delete'),

    # Check URLs
    path('checks/', CheckListView.as_view(), name='check-list'),
    path('checks/create/', CheckCreateView.as_view(), name='check-create
    path('checks/<int:pk>/update/', CheckUpdateView.as_view(), name='check-update'),
    path('checks/<int:pk>/delete/', CheckDeleteView.as_view(), name='check-delete'),

    # Order URLs
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/create/', OrderCreateView.as_view(), name='order-create'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('orders/<int:pk>/update/', OrderUpdateView.as_view(), name='order-update'),
    path('orders/<int:pk>/delete/', OrderDeleteView.as_view(), name='order-delete'),
]
