import random

from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from . tokens import generate_token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.contrib.auth.hashers import make_password
import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from twilio.rest import Client
from django.db.models import Sum, F
from django.shortcuts import render
from .models import Cart
from .models import *

stripe.api_key = settings.STRIPE_SECRET_KEY


TWILIO_ACCOUNT_SID = settings.TWILIO_ACCOUNT_SID
TWILIO_AUTH_TOKEN = settings.TWILIO_AUTH_TOKEN


def auth_view(request, type):
    if request.user.is_authenticated:
        return redirect('home') 
    if type == 'signup':
        return render(request, "components/auth.html", {'form_type': 'signup'})
    else:
        return render(request, "components/auth.html", {'form_type': 'login'})
    


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home') 
    if request.method == "POST":
        username = request.POST.get("username", None)
        password1 = request.POST.get("password1", None)
        email = request.POST.get("email", None)

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('home')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('home')
        
        if len(username)>20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('home')
        
        
        
        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('home')
        
        
        user = User.objects.create_user(username, email, password1)
        user.is_active = True
        user.save()
        messages.success(request, "Your account has been successfully created")
        return redirect('home')
    else:
        return render(request, "components/auth.html", {'form_type': 'signup'})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home') 
    if request.method == "POST":
        username = request.POST.get('user-login', None)
        password = request.POST.get('password', None)
        if not username or not password:
            messages.error(request, "Credentials are not provided!")
            return redirect('home')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Bad Credentials!")
            return redirect('home')
    return render(request, "components/auth.html", {'form_type': 'login'})


def signout(request):
    # Log out the user
    logout(request)

    messages.success(request, "Logged Out Successfully!")
    return redirect('home')


def forgot(request):
    if request.method == "POST":
        email = request.POST.get('pass-forgot')
        
        if email:
            try:
                user = User.objects.get(email=email)
                
                # Generate the unique URL for password reset
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                current_site = get_current_site(request)
                reset_url = reverse('change', kwargs={'uidb64': uid, 'token': token})
                reset_link = f'http://{current_site.domain}{reset_url}'
                
                mail_subject = 'Password Reset'
                # Render the email template with the reset link
                message = render_to_string('authentication/reset_password_email.html', {
                    'user': user,
                    'reset_link': reset_link,
                })

                # Send the password reset email to the user
                user.email_user(mail_subject, message)

                messages.success(request, "The password reset email has been sent successfully.")
                return redirect('home')

            except User.DoesNotExist:
                messages.error(request, "Sorry, the user with this email address is not registered.")
                return redirect('home')
        else:
            messages.error(request, "Please try to enter a valid email address next time.")
            return redirect('home')
    
    return render(request, "authentication/forgot.html")

@login_required(login_url='/auth/login/')
def change(request, uidb64, token):
    try:
        # Decode the uid from the URL and retrieve the user
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
        if default_token_generator.check_token(user, token):
            if request.method == "POST":
                password1 = request.POST.get('password1')
                password2 = request.POST.get('password2')

                if password1 and password2 and password1 == password2:
                    # Set the new password for the user
                    user.password = make_password(password1)
                    user.save()
                    messages.success(request, f"Password changed successfully for user: {user.username}")
                    return redirect('home')
                else:
                    messages.error(request, "Passwords do not match or some fields are empty. Please try again.")
                    return redirect('home')
            else:
                return render(request, "authentication/change_password.html", {'user': user, 'uidb64': uidb64, 'token': token})
        else:
            messages.error(request, "The password reset link is no longer valid.")
            return redirect('home')
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request, "The password reset link is no longer valid.")
        return redirect('home')


def activate(request, uidb64, token):
    try:
        # Decode the uidb64 parameter to get the user ID
        uid = urlsafe_base64_decode(uidb64).decode()
        # Get the user with the corresponding ID
        myuser = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        # Handle exceptions if the decoding or user retrieval fails
        myuser = None

    if myuser is not None and generate_token.check_token(myuser,token):
        # If the user exists and the token is valid
        myuser.is_active = True
        myuser.save() # Activate the user
        login(request,myuser) # Log in the user
        messages.success(request, "Your Account has been activated!")
        username = myuser.username
        return render(request, "authentication/index.html", {'username': username})
    else:
        # If the activation fails, render the activation failed template
        return render(request,'authentication/activation_failed.html')


@login_required(login_url='/auth/login/')
def landing_page_view(request):
    return render(request, "components/landing-page.html")

@login_required(login_url='/auth/login/')
def products_view(request, category):
    categories = SubCategory.objects.filter(main_category__name=category)
    products = Product.objects.filter(
        sub_category__main_category__name=category
    ).order_by("-created_at")

    paginator = Paginator(products, 12)
    page_number = request.GET.get("page")
    page_products = paginator.get_page(page_number)

    context = {
        "products": page_products,
        "categories": categories,
        "requested_category": category,
    }
    return render(request, "components/products.html", context)

@login_required(login_url='/auth/login/')
def filter_products_view(request, category, sub):
    categories = SubCategory.objects.filter(main_category__name=category)
    products = Product.objects.filter(sub_category__name=sub).order_by("-created_at")

    paginator = Paginator(products, 12)
    page_number = request.GET.get("page")
    page_products = paginator.get_page(page_number)

    context = {
        "products": page_products,
        "categories": categories,
        "requested_category": category,
        "selected_sub_category": sub,
    }
    return render(request, "components/products.html", context)

@login_required(login_url='/auth/login/')
def product_detail_view(request, pk):
    product = Product.objects.get(id=pk)
    context = {"product": product}
    return render(request, "components/single-product.html", context)

@login_required(login_url='/auth/login/')
def add_cart_view(request, pk, quantity):
    product = Product.objects.get(id=pk)
    # price = product.sale_price
    # total_price = price*quantity
    cart  = Cart.objects.get_or_create(
        user=request.user,
        product = product,
    )[0]
    cart.quantity =  quantity
    cart.save()
    messages.success(request, "Product added to cart")
    return redirect('user_cart')


@login_required(login_url='/auth/login/')
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    if not cart_items:
        messages.error(request, "Cart is empty, Add products to cart to view")
        return redirect("home")
    delivery_charges = 200
    total_product_price = cart_items.aggregate(
        total=Sum(F('quantity') * F('product__sale_price'))
    )['total'] or 0 
    total_price = delivery_charges + total_product_price
    context = {
        "cart_items": cart_items,
        "cart_items_count": cart_items.count(),
        "delivery_charges": delivery_charges,
        "total_product_price": total_product_price,
        "total_price": total_price,
    }
    return render(request, "components/cart.html", context)
    



def order_view(request):
    if request.method =="POST":
        phone_number = request.POST.get("phone_number")
        address_line1 = request.POST.get("address_line1")
        city = request.POST.get("city")
        state = request.POST.get("state")
        postal_code = request.POST.get("postal_code")
        address = Address.objects.create(
            user  =  request.user,
            phone_number = phone_number,
            address_line1 = address_line1,
            city = city,
            state = state,
            postal_code = postal_code,
            address_type = "shipping",
        )
        cart_items = Cart.objects.filter(user=request.user)
        total_product_price = cart_items.aggregate(
            total=Sum(F('quantity') * F('product__sale_price'))
        )['total'] or 0 
        import uuid
        Order.objects.create(
            user = request.user,
            shipping_address = address,
            billing_address = address,
            total_amount = total_product_price + 200,
            transaction_id=str(uuid.uuid4().int)[:5]
        )
        cart_items.delete()
        messages.success(request, "Order placed successfully")
        return redirect("user_cart")
    return redirect("user_cart")
    
        
        