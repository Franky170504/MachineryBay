from django.contrib import admin
from . models import Category, Customers, Products, SubCategory, Company

admin.site.register(Company)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Customers)
admin.site.register(Products)
