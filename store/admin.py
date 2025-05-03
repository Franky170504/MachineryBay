from django.contrib import admin
from .models import Company, Category, SubCategory, Customers, Products

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'company']
    list_filter = ['company']   # <-- This adds a filter in the right sidebar


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'category']
    list_filter = ['company', 'category']


@admin.register(Customers)
class CustomersAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name']


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'category', 'sub_category']
    list_filter = ['company', 'category', 'sub_category']
