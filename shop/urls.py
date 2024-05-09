from django.urls import path
from .views import ProductList, AllProductList, detail, logout_view, login_view, register, my_account

urlpatterns = [
    path('', ProductList.as_view(), name='index'),
    path('products/', AllProductList.as_view(), name='all_products'),
    path('product/<int:product_id>/', detail, name='detail'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register, name='register'),
    path('my_account/', my_account, name='my_account'),
]