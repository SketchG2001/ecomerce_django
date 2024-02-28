from django.db import models
import datetime


# Create your models here.

# Categories of products
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


# Customers model
class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# All of our products
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(default=0, max_digits=25, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=250, blank=True, default='', null=True)
    image = models.ImageField(upload_to='uploads/product')
    # Add sales stuffs
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, max_digits=25, decimal_places=2)


    def __str__(self):
        return self.name


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, )
    address = models.CharField(max_length=100, default='', null=False, blank=True)
    phone = models.CharField(max_length=10, default='', blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.product
