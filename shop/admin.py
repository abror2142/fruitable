from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Product, Comment, Rating, Region, City, Order, OrderProduct, Shipping

# Register your models here.


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'user', 'rating')
    list_display_links = ('id',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'user', 'created_at')
    list_display_links = ('id',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'quantity', 'category', 'get_image')
    list_display_links = ('name',)
    list_editable = ('price', 'quantity', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'description')

    def get_image(self, product):
        if product.image:
            return mark_safe(f'<img src="{product.image.url}" width="75px" style="border-radius: 15px;">')
        else:
            return 'Image not found'

    get_image.short_description = 'Rasmi'

    prepopulated_fields = {'slug': ('name', 'quantity')}
