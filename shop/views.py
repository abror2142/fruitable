from django.db.models import Count
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Category, Product, Rating, Comment
from .forms import RatingForm, RegisterForm, CommentForm
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
    extra_context = {
        'discounted_products': Product.objects.filter(discount__gt=0),
        'categories': Category.objects.filter(parent=None),
        'title': "Barcha Produclar"
    }


def detail(request, slug):
    product = Product.objects.get(slug=slug)
    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
    categories = Category.objects.filter(parent=product.category.parent).annotate(Count('products'))
    rating = 0
    comments = Comment.objects.filter(product=product)[:4]
    discounted_products = Product.objects.filter(discount__gt=0)
    # print(discounted_products)
    context = {
        'product': product,
        'user_rating': rating,
        'categories': categories,
        'comments': comments,
        'discounted_products': discounted_products
    }
    return render(request, 'shop/detail.html', context)


def rate(request: HttpRequest, product_id: int, rating: int) -> HttpResponse:
    product = Product.objects.get(pk=product_id)
    Rating.objects.filter(product=product, user=request.user).delete()
    product.rating_set.create(user=request.user, rating=rating)
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


def filter_view(request, filter_name):
    if filter_name == 'qimmat':
        products = Product.objects.order_by('-price')
    elif filter_name == 'arzon':
        products = Product.objects.order_by('price')
    else:
        products = Product.objects.all()
    categories = Category.objects.filter(parent=None)
    context = {
        'products': products,
        'categories': categories,
        'title': "Barcha Produclar"
    }

    return render(request, 'shop/all_products.html', context)


def sale_products_view(request):
    sale_products = Product.objects.filter(discount__gt=0)
    context = {
        'products': sale_products,
        'categories': Category.objects.filter(parent=None),
        'title': "Barcha Produclar"
    }
    return render(request, 'shop/all_products.html', context)