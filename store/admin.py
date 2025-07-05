from django.contrib import admin
from .models import Product, Category, Company

@admin.register(Category)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Company)
class ProductCompanyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'company', 'price', 'stock')
    list_filter = ('category', 'company')
    search_fields = ('name',)
