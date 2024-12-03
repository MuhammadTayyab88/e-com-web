import random

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

from .forms import *
from .models import *

stripe.api_key = settings.STRIPE_SECRET_KEY


TWILIO_ACCOUNT_SID = settings.TWILIO_ACCOUNT_SID
TWILIO_AUTH_TOKEN = settings.TWILIO_AUTH_TOKEN


def landing_page_view(request):
    return render(request, "components/landing-page.html")


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
