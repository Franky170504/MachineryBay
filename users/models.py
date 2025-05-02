from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.apps import apps
import datetime
import re

def validate_date_format(value):
    """Validate that the date is in dd-mm-yyyy format."""
    try:
        datetime.datetime.strptime(value, '%d-%m-%Y')
    except ValueError:
        raise ValidationError('Date must be in dd-mm-yyyy format.')
    
    # Additional check for the exact format
    if not re.match(r'^\d{2}-\d{2}-\d{4}$', value):
        raise ValidationError('Date must be in dd-mm-yyyy format.')

class User(AbstractUser):
    """Custom user model for customers."""
    
    # Override and add fields
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    date_of_birth = models.CharField(
        max_length=10, 
        validators=[validate_date_format],
        help_text="Date of birth in dd-mm-yyyy format"
    )
    customer_id = models.CharField(max_length=12, unique=True, blank=True)
    
    # Store model relationships will be handled through reverse relationships
    
    def save(self, *args, **kwargs):
        # Generate customer_id if it doesn't exist
        if not self.customer_id:
            self.customer_id = self._generate_customer_id()
        super().save(*args, **kwargs)
    
    def _generate_customer_id(self):
        """
        Generate a 12-digit alphanumeric customer ID:
        - First 3 letters from first name
        - First 3 letters from last name
        - First 2 digits of day, month, and year from DOB
        """
        if not all([self.first_name, self.last_name, self.date_of_birth]):
            raise ValidationError("First name, last name, and date of birth are required to generate customer ID")
        
        # Get first 3 letters from first and last name (or fewer if names are shorter)
        first_name_part = self.first_name[:3].upper()
        last_name_part = self.last_name[:3].upper()
        
        # Pad with 'X' if names are shorter than 3 characters
        first_name_part = first_name_part.ljust(3, 'X')
        last_name_part = last_name_part.ljust(3, 'X')
        
        # Parse date components
        try:
            day, month, year = self.date_of_birth.split('-')
            date_part = day[:2] + month[:2] + year[:2]
        except (ValueError, IndexError):
            raise ValidationError("Date of birth must be in dd-mm-yyyy format")
        
        # Combine all parts to form the customer ID
        customer_id = f"{first_name_part}{last_name_part}{date_part}"
        
        return customer_id
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.customer_id})"
        
    def get_bookmarked_products(self):
        """Get all bookmarked products for this user."""
        Products = apps.get_model('store', 'Products')
        return Products.objects.filter(bookmarked_by_users=self)
    
    def get_viewed_products(self):
        """Get all viewed products for this user."""
        ProductView = apps.get_model('store', 'ProductView')
        return ProductView.objects.filter(user=self).select_related('product')
    
    def bookmark_product(self, product):
        """Add a product to bookmarks."""
        product.bookmarked_by_users.add(self)
    
    def remove_bookmark(self, product):
        """Remove a product from bookmarks."""
        product.bookmarked_by_users.remove(self)
    
    def record_product_view(self, product):
        """Record that user viewed a product."""
        ProductView = apps.get_model('store', 'ProductView')
        ProductView.objects.create(user=self, product=product)
    
    def link_store_customer(self, store_customer):
        """Link this user to a store.Customers record."""
        if hasattr(store_customer, 'user') and store_customer.user is not None:
            raise ValueError("This customer is already linked to a user")
        
        store_customer.user = self
        store_customer.save()
        
        # Optionally sync data
        if not self.first_name:
            self.first_name = store_customer.first_name
        if not self.last_name:
            self.last_name = store_customer.last_name
        if not self.email:
            self.email = store_customer.email
        self.save()
        
        return True

    @classmethod
    def create_from_store_customer(cls, store_customer, username, password=None, date_of_birth=None):
        """Create a new User from a store.Customers instance."""
        if not date_of_birth:
            raise ValueError("date_of_birth is required to generate customer_id")
            
        user = cls(
            username=username,
            first_name=store_customer.first_name,
            last_name=store_customer.last_name,
            email=store_customer.email,
            date_of_birth=date_of_birth
        )
        
        if password:
            user.set_password(password)
        
        user.save()
        
        # Link the store customer to this user
        store_customer.user = user
        store_customer.save()
        
        return user