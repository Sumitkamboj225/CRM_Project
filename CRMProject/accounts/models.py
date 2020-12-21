from django.db import models
from django.contrib.auth.models import User

class Customers(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    name=models.CharField(max_length=100,null=True)
    email=models.EmailField(max_length=100,null=True)
    mobile=models.BigIntegerField(null=True)
    created_date=models.DateField(auto_now_add=True,null=True)
    def __str__(self):
        return self.name

class Products(models.Model):
    CATEGORY=(
        ('Indoor','Indoor'),
        ('Outdoor','Outdoor'),
        ('Anywhere','Anywhere')
    )
    name=models.CharField(max_length=100,null=True)
    price=models.FloatField(null=True)
    created_date=models.DateField(auto_now_add=True,null=True)
    description=models.CharField(blank=True,max_length=100)
    category=models.CharField(choices=CATEGORY,null=True,max_length=100)
    image=models.ImageField(default="",upload_to='images',)
    def __str__(self):
        return self.name

class Orders(models.Model):
    STATUS=(
        ('Delivered','Delivered'),
        ('Pending','Pending'),
        ('OutForDelivery','OutForDelivery')
    )
    customer=models.ForeignKey(Customers,on_delete=models.CASCADE,null=True)
    product=models.ForeignKey(Products,on_delete=models.CASCADE,null=True)
    status=models.CharField(max_length=100,choices=STATUS,null=True)
    created_date=models.DateField(auto_now_add=True,null=True)
    def __str__(self):
        return str(self.product)