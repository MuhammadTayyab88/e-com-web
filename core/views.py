from django.shortcuts import render, redirect, get_object_or_404
from .models import HomePageImage, Product, CartItem,TrackingOrder,PhoneOTP
from django.contrib.auth.decorators import login_required
from .forms import CartItemForm, CheckoutForm, RegisterForm, LoginForm, ContactForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from twilio.rest import Client
from django.conf import settings
import stripe
from django.contrib.auth.models import User
import random
import datetime
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .models import TrackingOrder
from django.contrib.auth.forms import UserCreationForm

from django.http import JsonResponse

stripe.api_key = settings.STRIPE_SECRET_KEY



# Access the model using get_model in the function where needed



# views.py
def home(request):
    homepage_images = HomePageImage.objects.all()
    categories = ["clothes", "watches", "fashion", "electronics"]
    products_by_category = {}

    # Loop through each category to get exactly three random products or all if fewer than three
    for category in categories:
        products = list(Product.objects.filter(category__iexact=category))

        # Select three random products or all products if fewer than three are available
        if len(products) > 3:
            products = random.sample(products, 3)
        products_by_category[category] = products

    return render(request, 'index.html', {
        'homepage_images': homepage_images,
        'products_by_category': products_by_category,
    })



#your view to handle the form submission and save the data to the database.
def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        size = request.POST.get('size')  # Size field (for Clothes category)
        quantity = request.POST.get('quantity')

        # Check if the product exists
        product = get_object_or_404(Product, id=product_id)

        # Validate quantity
        if not quantity or int(quantity) <= 0:
            messages.error(request, 'Please enter a valid quantity.')
            return redirect(request.META.get('HTTP_REFERER', 'home'))

        # Only require size selection if the product category is "clothes"
        if product.category == "clothes" and not size:
            messages.error(request, 'Please select a size for this product.')
            return redirect(request.META.get('HTTP_REFERER', 'home'))

        # Create or update the cart item with or without size
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            size=size,
            quantity= quantity
        )

        # If the cart item already exists, update the quantity
        if not created:
            cart_item.quantity += int(quantity)
            cart_item.save()

        messages.success(request, f"{product.name} has been added to your cart.")
        return redirect('cart')  # Redirect to the cart page

    return redirect('index')

def remove_from_cart(request, item_id):
    # Find the cart item based on the provided item_id and ensure it belongs to the logged-in user
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)

    # Delete the cart item
    cart_item.delete()

    # Display a success message
    messages.success(request, "Item has been removed from your cart.")

    # Redirect back to the cart page
    return redirect('cart')

@login_required
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    cart_subtotal = sum(item.product.price * item.quantity for item in cart_items)
    delivery_fee = 150
    cart_total = cart_subtotal + delivery_fee
    
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'cart_subtotal': cart_subtotal,
        'delivery_fee': delivery_fee,
        'cart_total': cart_total,
    })
    
def checkout_success(request):
    return render(request,'checkout_success.html')



def register(request):
    if request.method == 'POST':
        phone_number = request.POST['phone']
        otp = request.POST['otp']

        # Verify OTP
        try:
            otp_entry = PhoneOTP.objects.get(phone_number=phone_number, otp=otp)
        except PhoneOTP.DoesNotExist:
            return JsonResponse({'status': 'fail', 'message': 'OTP verification failed'})

        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Remove OTP entry after successful registration
            otp_entry.delete()
            return JsonResponse({'status': 'success', 'message': 'Registration successful'})

    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Hello ! {username}.')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    print("User before logout:", request.user)
    logout(request)
    print("User after logout:", request.user)
    messages.success(request, 'You have successfully logged out.')
    return redirect('/')




def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            send_mail(
                f'Message from {name}',
                message,
                email,
                ['Tayyibmuhammad1414@gmail.com'],  # Replace with your admin email
                fail_silently=False,
            )
            return redirect('home')
    else:
        form = ContactForm()
    return render(request, 'contact_us.html', {'form': form})


def send_order_confirmation_sms(user_phone, order_id):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = f'Thank you for your order! Your order has been placed.Thankyou for shopping.Your Order id is {order_id}.'
    client.messages.create(
        body=message,
        from_=settings.TWILIO_PHONE_NUMBER,
        to=user_phone
    )


def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    cart_subtotal = sum(item.product.price * item.quantity for item in cart_items)
    delivery_fee = 150
    cart_total = cart_subtotal + delivery_fee

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            payment_method = form.cleaned_data.get('payment_method')

            for cart_item in cart_items:
                checkout_info = form.save(commit=False)
                checkout_info.user = request.user
                checkout_info.product = cart_item.product
                checkout_info.size = cart_item.size
                checkout_info.quantity = cart_item.quantity
                checkout_info.save()

                if payment_method == 'online':
                    amount_in_cents = int(cart_total * 100)
                    if amount_in_cents <= 99999999: 
                        session = stripe.checkout.Session.create(
                            payment_method_types=['card'],
                            line_items=[{
                                'price_data': {
                                    'currency': 'usd',
                                    'product_data': {
                                        'name': f"{checkout_info.product.name} ({checkout_info.size})",
                                    },
                                    'unit_amount': int(checkout_info.product.price * 100),
                                },
                                'quantity': checkout_info.quantity,
                            }],
                            mode='payment',
                            success_url=request.build_absolute_uri('checkout_success'),
                            cancel_url=request.build_absolute_uri('checkout'),
                        )
                        return redirect(session.url, code=303)
                    else:
                        messages.error(request, 'The total amount exceeds the allowed limit.')
                        return redirect('checkout')
                else:
                    send_order_confirmation_sms(checkout_info.contact_number, checkout_info.id)

            cart_items.delete()  # Clear all items from cart after processing

            messages.success(request, 'Your order has been placed successfully!')
            return redirect('checkout_success')
    else:
        form = CheckoutForm()

    return render(request, 'checkout.html', {
        'form': form,
        'cart_items': cart_items,
        'cart_total': cart_total,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
    })

@login_required
def track_order(request):
    order_status = None
    error_message = None

    if request.method == 'POST':
        tracking_number = request.POST.get('tracking-number').strip()
        
        if tracking_number:
            try:
                order = TrackingOrder.objects.get(tracking_number=tracking_number, user=request.user)
                order_status = {
                    'status': order.get_status_display(),
                    'tracking_number': order.tracking_number,
                    'tracking_url': order.tracking_url,
                    'order_date': order.order_date
                }
            except TrackingOrder.DoesNotExist:
                error_message = "Order not found. Please wait your status will be updated shortly."
        else:
            error_message = "Please enter a valid tracking number."

    return render(request, 'track_order.html', {
        'order_status': order_status,
        'error_message': error_message
    })

VALID_CATEGORIES = ['clothes', 'watches', 'fashion', 'electronics']


def category_page(request, category_name):
    # Check if the request is POST for handling form submissions, like size validation
    if request.method == 'POST':
        size = request.POST.get('size')
        # Check if the category is clothes and no size is selected
        if category_name.lower() == "clothes" and not size:
            messages.error(request, 'Please select a size for this product.')
            return redirect(request.META.get('HTTP_REFERER', 'home'))

    # Retrieve products based on category (this will run regardless of GET or POST)
    category_products = Product.objects.filter(category__iexact=category_name)
    print(f"Category: {category_name}, Products: {category_products}")  # Debugging output
    
    return render(request, 'category_page.html', {
        'category_name': category_name.capitalize(),
        'category_products': category_products,
        'is_clothes_category': category_name.lower() == 'clothes',
        'is_fashion_category': category_name.lower() == 'fashion',
        'is_electronics_category': category_name.lower() == 'electronics',
    })
def forget_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
            return redirect('reset_password', email=user.email)
        except User.DoesNotExist:
            messages.error(request, "Email not found in the database.")
            return redirect('forget_password')
    return render(request, 'forget.html')

def reset_password(request, email):
    if request.method == 'POST':
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        if new_password == confirm_password:
            user = User.objects.get(email=email)
            user.password = make_password(new_password)
            user.save()
            messages.success(request, "Password has been reset successfully.")
            return redirect('login')
        else:
            messages.error(request, "Passwords do not match.")
            return redirect('reset_password', email=email)
    return render(request, 'reset_password.html', {'email': email})

def send_otp(phone_number):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    otp = str(random.randint(1000, 9999))  # Generate a 4-digit OTP

    # Store OTP in database (overwrite if it exists)
    PhoneOTP.objects.update_or_create(phone_number=phone_number, defaults={'otp': otp})
    
    # Send the OTP using Twilio
    message = client.messages.create(
        body=f"Your OTP is {otp}",
        from_=settings.TWILIO_PHONE_NUMBER,
        to=phone_number
    )
    return otp

# View to send OTP
def send_otp_view(request):
    phone_number = request.GET.get('phone')
    if not phone_number:
        return JsonResponse({'status': 'fail', 'message': 'Phone number is required'})

    # Send the OTP
    send_otp(phone_number)
    return JsonResponse({'status': 'success', 'message': 'OTP sent successfully'})

# View to verify OTP
def verify_otp_view(request):
    phone_number = request.GET.get('phone')
    otp = request.GET.get('otp')
    try:
        otp_entry = PhoneOTP.objects.get(phone_number=phone_number, otp=otp)
        # Optional: Check OTP expiry
        if otp_entry.created_at < datetime.datetime.now() - datetime.timedelta(minutes=10):
            return JsonResponse({'status': 'fail', 'message': 'OTP expired'})
        
        return JsonResponse({'status': 'success', 'message': 'OTP verified successfully'})
    except PhoneOTP.DoesNotExist:
        return JsonResponse({'status': 'fail', 'message': 'Invalid OTP'})