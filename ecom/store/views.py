import json

from django.shortcuts import render, redirect
from . import models
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from django import forms
from django.db.models import Q
from cart.cart import Cart


# Create your views here.

def search(request):
    if request.method == 'POST':
        searched = request.POST.get('searchead', '')  # Use get() to avoid KeyError
        searched_products = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
        if not searched_products:
            messages.success(request, "That product doesn't exist... Please try again.")
        return render(request, "search.html", {'searchead': searched_products})
    else:
        return render(request, "search.html", {})


def update_info(request):
    if request.user.is_authenticated:
        current_user = request.user.profile
        form = UserInfoForm(request.POST or None, instance=current_user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your info has been updated!!')
            return redirect('home')
        return render(request, "update_info.html", {"form": form})
    else:
        messages.success(request, 'You must be logged in to access this page.')
        return redirect('home')


def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your password has been updated successfully!')
                login(request, current_user)
                return redirect('update_password')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
        else:
            form = ChangePasswordForm(current_user)
        return render(request, 'update_password.html', {'form': form})
    else:
        messages.success(request, 'You must be logged in to access this page.')
        return redirect('home')


def update_user(request):
    if request.user.is_authenticated:
        current_user = request.user
        user_form = UpdateUserForm(request.POST or None, instance=current_user)
        if user_form.is_valid():
            user_form.save()
            login(request, current_user)
            messages.success(request, 'Your account has been updated!!')
            return redirect('home')
        return render(request, "update_user.html", {"user_form": user_form})
    else:
        messages.success(request, 'You must be logged in to access this page.')
        return redirect('home')


def category_summary(request):
    categories = Category.objects.all()
    return render(request, "category_summary.html", {"categories": categories})


def category(request, foo):
    foo = foo.replace("-", " ")
    try:
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, "category.html", {"products": products, "category": category})
    except Category.DoesNotExist:
        messages.success(request, "Sorry, I couldn't find")
        return redirect("home")


def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, "product.html", {"product": product})


def home(request):
    products = Product.objects.all()
    return render(request, "index.html", {"products": products})


def about(request):
    return render(request, "about.html")


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            current_user = Profile.objects.get(user=user)
            saved_cart = current_user.old_cart
            if saved_cart:
                converted_cart = json.loads(saved_cart)
                cart = Cart(request)
                for key, value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)
            messages.success(request, "You are now logged in")
            return redirect("home")
        else:
            messages.error(request, "There was an error, Please try again")
            return redirect("login")
    else:
        return render(request, "login.html")


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out successfully!")
    return redirect("home")


def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Username created - Please Fill out Your info below...")
            return redirect("update_info")
        else:
            messages.error(request, "There was a problem registering please try again")
            return redirect("register")
    else:
        return render(request, "register.html", {"form": form})
