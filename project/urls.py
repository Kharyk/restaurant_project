from django.urls import path
from project import views
from project.views import (
    # SearchResultsView,
    LoginView,
    CustomLogoutView,
    SignupView,
    HomepageView,
    LearnMoreView,
    ContactView,
    AboutUsView,
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
    # DishPriceListView,
    DishPriceDetailView,
    # DishPriceUpdateView,
    # DishPriceDeleteView,
    TablePriceCreateView,
    # TablePriceListView,
    TablePriceDetailView,
    # TablePriceUpdateView,
    # TablePriceDeleteView,
    CommentCreateView,
    CommentUpdateView,
    CommentDeleteView,
    StarsCreateView,
    StarsUpdateView,
    StarsDeleteView,
    CheckCreateView,
    CheckCurrentListView,
    CheckInProcessListView,
    CheckHistoryListView,
    CheckDetailView,
    CheckUpdateView,
    CheckDeleteView,
    OrderCreateView,
    OrderListView,
    OrderDetailView,
    OrderUpdateView,
    OrderDeleteView,
    CheckWaiterListView,
    change_status_pay, 
    change_status_done,
    dish_search, 
    CartOfPrivilegesListView, 
    CartOfPrivilegesDetailView, 
    CartOfPrivilegesCreateView, 
    CartOfPrivilegesUpdateView, 
    CartOfPrivilegesDeleteView, 
    AllergiesListView, 
    # AllergiesDetailView, 
    AllergiesCreateView, 
    AllergiesDeleteView, 
    LanguageOfCommunicationListView, 
    # LanguageOfCommunicationDetailView, 
    LanguageOfCommunicationCreateView, 
    LanguageOfCommunicationDeleteView, 
    ExtraInfoUserCreateView, 
    ExtraInfoUserDetailView, 
    ExtraInfoUserUpdateView, 
    ExtraInfoUserDeleteView
)

urlpatterns = [
    path('', HomepageView.as_view(), name='home'),
    path('learn-more/', LearnMoreView.as_view(), name='learn-more'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('about-us/', AboutUsView.as_view(), name='about-us'),

    
    
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),

    path('search/', views.dish_search, name='search-results'),

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
    # path('dish-prices/', DishPriceListView.as_view(), name='dish-price-list'),
    path('dish/<int:pk>/dish-prices/create/', DishPriceCreateView.as_view(), name='dish-price-create'), 
    path('dish-prices/<int:pk>/', DishPriceDetailView.as_view(), name='dish-price-detail'),
    # path('dish-prices/<int:pk>/update/', DishPriceUpdateView.as_view(), name='dish-price-update'),
    # path('dish-prices/<int:pk>/delete/', DishPriceDeleteView.as_view(), name='dish-price-delete'),

    # Table Price URLs
    # path('table-prices/', TablePriceListView.as_view(), name='table-price-list'),
    path('table/<int:pk>/table-prices/create/', TablePriceCreateView.as_view(), name='table-price-create'),
    path('table-prices/<int:pk>/', TablePriceDetailView.as_view(), name='table-price-detail'),
    # path('table-prices/<int:pk>/update/', TablePriceUpdateView.as_view(), name='table-price-update'),
    # path('table-prices/<int:pk>/delete/', TablePriceDeleteView.as_view(), name='table-price-delete'),

    # Comment URLs
    path('comments/create/', CommentCreateView.as_view(), name='comment-create'),
    path('comments/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),
    path('comments/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),

    # Stars URLs
    path('stars/create/', StarsCreateView.as_view(), name='stars-create'),
    path('stars/<int:pk>/update/', StarsUpdateView.as_view(), name='stars-update'),
    path('stars/<int:pk>/delete/', StarsDeleteView.as_view(), name='stars-delete'),

    # Check URLs
    path('checks/current/', CheckCurrentListView.as_view(), name='check-current'),
    path('checks/process/', CheckInProcessListView.as_view(), name='check-process'),
    path('checks/history', CheckHistoryListView.as_view(), name='check-history'),
    path('checks/create/', CheckCreateView.as_view(), name='check-create'),
    path('checks/<int:pk>/update/', CheckUpdateView.as_view(), name='check-update'),
    path('checks/<int:pk>', CheckDetailView.as_view(), name='check-detail'),
    path('checks/<int:pk>/delete/', CheckDeleteView.as_view(), name='check-delete'),
    
    #Waiter URLs
    path('waiter/checks/', CheckWaiterListView.as_view(), name='waiter-check-list'),
    path('change-status-pay/<int:check_id>/', change_status_pay, name='change_status_pay'),
    path('change-status-done/<int:check_id>/', change_status_done, name='change_status_done'),



    # Order URLs
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/create/<int:pk>', OrderCreateView.as_view(), name='order-create'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('orders/<int:pk>/update/', OrderUpdateView.as_view(), name='order-update'),
    path('orders/<int:pk>/delete/', OrderDeleteView.as_view(), name='order-delete'),
    
    # CartOfPrivileges URLs
    path('privileges/', views.CartOfPrivilegesListView.as_view(), name='cart-privileges-list'),
    path('privileges/new/', views.CartOfPrivilegesCreateView.as_view(), name='cart-privileges-create'),
    path('privileges/<int:pk>/', views.CartOfPrivilegesDetailView.as_view(), name='cart-privileges-detail'),
    path('privileges/<int:pk>/update/', views.CartOfPrivilegesUpdateView.as_view(), name='cart-privileges-update'),
    path('privileges/delete/<int:pk>/', views.CartOfPrivilegesDeleteView.as_view(), name='cart-privileges-delete'),

    # Allergies URLs
    path('allergies/', views.AllergiesListView.as_view(), name='allergies-list'),
    path('allergies/new/', views.AllergiesCreateView.as_view(), name='allergies-create'),
    # path('allergies/<int:pk>/', views.AllergiesDetailView.as_view(), name='allergies-detail'),
    path('allergies/<int:pk>/', views.AllergiesDeleteView.as_view(), name='allergies-delete'),

    # Language URLs
    path('languages/', views.LanguageOfCommunicationListView.as_view(), name='language-list'),
    # path('languages/<int:pk>/', views.LanguageOfCommunicationDetailView.as_view(), name='language-detail'),
    path('languages/new/', views.LanguageOfCommunicationCreateView.as_view(), name='language-create'),
    path('languages/<int:pk>/', views.LanguageOfCommunicationDeleteView.as_view(), name='language-delete'),
    

    # Extra Info User URLs
    path('extra-info/<int:pk>/', views.ExtraInfoUserDetailView.as_view(), name='extra-info-detail'),
    path('extra-info/<int:pk>/update/', views.ExtraInfoUserUpdateView.as_view(), name='extra-info-update'),
    path('extra-info/new/', views.ExtraInfoUserCreateView.as_view(), name='extra-info-create'),
    path('extra-info/<int:pk>/delete/', views.ExtraInfoUserDeleteView.as_view(), name='extra-info-delete'),

]