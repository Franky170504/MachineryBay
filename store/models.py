from django.db import models
import datetime

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class SubCategory(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default= 1)

    def __str__(self):
        return self.name
    
class Customers(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    mobile_no = models.IntegerField(max_length=10)
    email = models.EmailField(max_length=100)
    password = models.CharField

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
class Products(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default= 1)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, default= 1)
    description = models.CharField(max_length=500)
    image = models.ImageField(upload_to='uploads/products/')

    def __str__(self):
        return self.name
    

