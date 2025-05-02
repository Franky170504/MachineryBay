from django.db import models
from django.conf import settings
import datetime

class Company(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "companies"
    
class Category(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "categories"

class SubCategory(models.Model):
    name = models.CharField(max_length=50)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, default=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Sub Categories"
    
class Customers(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    mobile_no = models.IntegerField()  # Removed max_length as it's not valid for IntegerField
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=128, blank=True, null=True)  # Fixed incomplete field
    # Add reference to the User model if needed
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='store_customer_profile'
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    class Meta:
        verbose_name_plural = "customers"
    
class Products(models.Model):
    name = models.CharField(max_length=50)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, default=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=500)
    image = models.ImageField(upload_to='uploads/products/')
    # Add fields for bookmarks and view history
    bookmarked_by_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='bookmarked_store_products',
        blank=True
    )

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "products"

# New model to track product views
class ProductView(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='views')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='product_views')
    viewed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-viewed_at']
        verbose_name = "Product View"
        verbose_name_plural = "Product Views"
        
    def __str__(self):
        return f"{self.user.username} viewed {self.product.name} on {self.viewed_at}"