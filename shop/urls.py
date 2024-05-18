from django.urls import path
from .views import (ProductList, AllProductList, detail, logout_view, login_view, register,
                    my_account, rate, filter_view, sale_products_view, to_cart, cart,
                    create_checkout_session, success_payment)

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
    path('sale_products/', sale_products_view, name='sale_products'),
    path('cart/', cart, name='cart'),
    path('to-cart/<int:product_id>/<str:action>/', to_cart, name='to_cart'),
    path('payment/', create_checkout_session, name='payment'),
    path('success/', success_payment, name='success_payment')
]