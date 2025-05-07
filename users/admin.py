from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomerMetadata, BookmarkedProduct, ViewHistory

@admin.register(CustomerMetadata)
class CustomerMetadataAdmin(admin.ModelAdmin):
    list_display = ('customer_id', 'first_name', 'last_name', 'date_of_birth')
    search_fields = ('customer_id', 'first_name', 'last_name')
    list_filter = ('date_of_birth',)

@admin.register(BookmarkedProduct)
class BookmarkedProductAdmin(admin.ModelAdmin):
    list_display = ('customer', 'product_id', 'bookmarked_at')
    search_fields = ('customer__customer_id', 'product_id')
    list_filter = ('bookmarked_at',)

@admin.register(ViewHistory)
class ViewHistoryAdmin(admin.ModelAdmin):
    list_display = ('customer', 'product_id', 'product_company', 'product_category', 'view_count', 'viewed_at')
    search_fields = ('customer__customer_id', 'product_id', 'product_company', 'product_category')
    list_filter = ('product_company', 'product_category', 'viewed_at')

