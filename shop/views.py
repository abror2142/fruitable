from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Category, Product
from .forms import RatingForm, RegisterForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User


class ProductList(ListView):
    model = Product
    template_name = 'shop/index.html'
    context_object_name = 'products'
    extra_context = {
        'categories': Category.objects.filter(parent=None),
        'title': "Barcha Produclar"
    }


class AllProductList(ProductList):
    template_name = 'shop/all_products.html'


def detail(request, product_id):
    product = Product.objects.get(pk=product_id)
    if request.method == 'POST' and request.user.is_authenticated:
        data = {
            'user': User.objects.get(username=request.user),
            'product': product,
            'rating': request.POST['rating']
        }
        form = RatingForm(data=data)
        if form.is_valid():
            print(data)
            form.save()
            return redirect('index')
    rating = RatingForm()
    context = {
        'product': product,
        'rating': rating
    }
    return render(request, 'shop/detail.html', context=context)


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
    return render(request, 'shop/login.html')


def logout_view(request):
    logout(request)
    return redirect('index')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    form = RegisterForm()
    context = {
        'form': form
    }
    return render(request, 'shop/register.html', context=context)


def my_account(request):
    return render(request, 'shop/profile.html')




