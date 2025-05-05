from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import CustomerMetadata, BookmarkedProduct, ViewHistory

# Define an inline admin descriptor for CustomerMetadata model
class CustomerMetadataInline(admin.StackedInline):
    model = CustomerMetadata
    can_delete = False
    verbose_name_plural = 'customer metadata'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (CustomerMetadataInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(CustomerMetadata)
class CustomerMetadataAdmin(admin.ModelAdmin):
    list_display = ('customer_id', 'first_name', 'last_name', 'date_of_birth', 'phone_number')
    search_fields = ('customer_id', 'first_name', 'last_name', 'phone_number')
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

