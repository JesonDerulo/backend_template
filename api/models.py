from django.db import models

# Create your models here.
# models.py
from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # Add more properties as needed
    # Example: image = models.ImageField(upload_to='product_images/')
    def __str__(self):
        return str(self.name)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True )
    totalPrice = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    isPaid = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)



class OrderItem(models.Model):
    # connect to Product Model
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    # connect to Order Model:
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    _id  = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return str(self.name)