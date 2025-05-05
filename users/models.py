from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomerMetadata(models.Model):
    """
    Model for storing customer metadata, separate from but linked to the default User model.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='metadata'
    )
    
    first_name = models.CharField(
        _('first name'), 
        max_length=150, 
        blank=True
    )
    
    last_name = models.CharField(
        _('last name'), 
        max_length=150, 
        blank=True
    )
    
    customer_id = models.CharField(
        _('customer ID'),
        max_length=12,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z0-9]{12}$',
                message=_('Customer ID must be exactly 12 alphanumeric characters.')
            )
        ],
        help_text=_('12-digit alphanumeric customer ID'),
        blank=True
    )
    
    date_of_birth = models.DateField(
        _('date of birth'),
        help_text=_('Format: DD-MM-YYYY'),
        null=True,
        blank=True
    )
    
    phone_number = models.CharField(
        _('phone number'),
        max_length=15,
        blank=True,
        null=True
    )
    
    class Meta:
        verbose_name = _('customer metadata')
        verbose_name_plural = _('customer metadata')
    
    def save(self, *args, **kwargs):
        # Generate customer_id if not provided
        if not self.customer_id and self.first_name and self.last_name and self.date_of_birth:
            self.customer_id = self._generate_customer_id()
        super().save(*args, **kwargs)
    
    def _generate_customer_id(self):
        """Generate a 12-digit alphanumeric customer ID:
        - First 3 letters from first name
        - First 3 letters from last name
        - First 2 digits of date, month and year from DoB
        """
        # Get first 3 letters from first name (padded with 'x' if shorter)
        first_name_part = self.first_name.lower()[:3].ljust(3, 'x')
        
        # Get first 3 letters from last name (padded with 'x' if shorter)
        last_name_part = self.last_name.lower()[:3].ljust(3, 'x')
        
        # Get date components
        day_part = str(self.date_of_birth.day).zfill(2)[:2]
        month_part = str(self.date_of_birth.month).zfill(2)[:2]
        year_part = str(self.date_of_birth.year)[-2:]
        
        # Combine all parts
        customer_id = f"{first_name_part}{last_name_part}{day_part}{month_part}{year_part}"
        
        return customer_id
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.customer_id})"


class BookmarkedProduct(models.Model):
    """Model to store products bookmarked by customers."""
    customer = models.ForeignKey(
        CustomerMetadata,
        on_delete=models.CASCADE,
        related_name='bookmarked_products'
    )
    product_id = models.PositiveIntegerField()
    bookmarked_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('customer', 'product_id')
        verbose_name = _('bookmarked product')
        verbose_name_plural = _('bookmarked products')
    
    def __str__(self):
        return f"{self.customer.customer_id} - Product {self.product_id}"


class ViewHistory(models.Model):
    """Model to store products viewed by customers."""
    customer = models.ForeignKey(
        CustomerMetadata,
        on_delete=models.CASCADE,
        related_name='view_history'
    )
    product_id = models.PositiveIntegerField()
    product_category = models.CharField(max_length=100, blank=True, null=True)
    product_company = models.CharField(max_length=100, blank=True, null=True)
    viewed_at = models.DateTimeField(auto_now_add=True)
    view_count = models.PositiveIntegerField(default=1)
    
    class Meta:
        verbose_name = _('view history')
        verbose_name_plural = _('view histories')
    
    def __str__(self):
        return f"{self.customer.customer_id} - Product {self.product_id} ({self.view_count} views)"


@receiver(post_save, sender=User)
def create_customer_metadata(sender, instance, created, **kwargs):
    """
    Create CustomerMetadata record when a User is created.
    This ensures every user has associated metadata.
    """
    if created:
        # Use User's first and last name for initial metadata
        CustomerMetadata.objects.create(
            user=instance,
            first_name=instance.first_name,
            last_name=instance.last_name
        )


@receiver(post_save, sender=User)
def save_customer_metadata(sender, instance, **kwargs):
    """
    Update CustomerMetadata when User is saved.
    This keeps first name and last name in sync if they're updated on the User model.
    """
    if hasattr(instance, 'metadata'):
        # Only sync these fields if they're changed at the User level
        if instance.metadata.first_name != instance.first_name:
            instance.metadata.first_name = instance.first_name
        if instance.metadata.last_name != instance.last_name:
            instance.metadata.last_name = instance.last_name
        instance.metadata.save()