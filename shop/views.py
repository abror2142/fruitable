from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Category, Product, Rating
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


def detail(request, slug):
    product = Product.objects.get(slug=slug)
    categories = Category.objects.filter(parent=product.category.parent)
    product_count = []
    for category in categories:
        product_count.append({'name': category.name, 'count': len(category.products.all()), 'slug': category.slug})

    try:
        rating = Rating.objects.get(product=product, user=request.user).rating
    except Rating.DoesNotExist:
        rating = 0
    context = {
        'product': product,
        'user_rating': rating,
        'product_count': product_count
    }

    return render(request, 'shop/detail.html', context)


def rate(request: HttpRequest, product_id: int, rating: int) -> HttpResponse:
    print(product_id, rating)
    product = Product.objects.get(pk=product_id)
    Rating.objects.filter(product=product, user=request.user).delete()
    product.rating_set.create(user=request.user, rating=rating)
    print(product.rating_set, request.user)
    return redirect('detail', slug=product.slug)


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
