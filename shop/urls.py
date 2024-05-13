from django.urls import path
from .views import (ProductList, AllProductList, detail, logout_view, login_view, register,
                    my_account, rate, filter_view, sale_products_view)

urlpatterns = [
    path('', ProductList.as_view(), name='index'),
    path('products/', AllProductList.as_view(), name='all_products'),
    path('products/filter/<str:filter_name>/', filter_view, name='filter_name'),
    path('product/<slug:slug>/', detail, name='detail'),
    path('rate/<int:product_id>/<int:rating>/', rate),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register, name='register'),
    path('my_account/', my_account, name='my_account'),
    path('sale_products/', sale_products_view, name='sale_products')
]