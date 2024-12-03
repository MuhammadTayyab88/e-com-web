from django.urls import path
from .views import home, add_to_cart, cart, register, login_view, contact_view, logout_view, track_order
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home, name='home'),
    path('add-to-cart/', add_to_cart, name='add_to_cart'),
    path('cart/', cart, name='cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/success/', views.checkout_success, name='checkout_success'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('contact/', contact_view, name='contact_view'),
    path('track-order/', track_order, name='track_order'),
    path('category/<str:category_name>/', views.category_page, name='category_page'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('register/', views.register, name='register'), 
     path('password-reset/', auth_views.PasswordResetView.as_view(template_name='forget.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('reset_password/<str:email>/', views.reset_password, name='reset_password'),
    path('forget_password/', views.forget_password, name='forget_password'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('category/<str:category_name>/', views.category_page, name='category_page'),
]