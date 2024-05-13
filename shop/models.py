from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum, Avg
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name="Kategoriya", unique=True)
    image = models.ImageField(upload_to='category/', null=True, blank=True)
    slug = models.SlugField(blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE,
                               null=True, blank=True,
                               related_name='subcategories')

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name="Nomi")
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    price = models.FloatField()
    image = models.ImageField(upload_to='products/')
    quantity = models.IntegerField(default=0)
    slug = models.SlugField(blank=True, null=True)
    discount = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    @property
    def discounted_price(self):
        d_price = self.price - self.price * self.discount / 100
        return d_price

    @property
    def avg_rating(self):
        rating = self.rating_set.all().aggregate(Avg('rating'))
        return round(rating['rating__avg'] or 0)


RATES = {
    '1': 1,
    "2": 2,
    "3": 3,
    '4': 4,
    '5': 5
}


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product.name}: {self.rating}"


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField()

    def __str__(self):
        return self.content[:20]

