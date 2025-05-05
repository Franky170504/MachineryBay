from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import CustomerMetadata, BookmarkedProduct, ViewHistory


class DateInput(forms.DateInput):
    """Custom DateInput widget with HTML5 date input type."""
    input_type = 'date'


class CustomerMetadataForm(forms.ModelForm):
    """
    Form for updating customer metadata.
    """
    date_of_birth = forms.DateField(
        widget=DateInput(),
        help_text='Enter date in DD-MM-YYYY format',
        required=True
    )
    
    class Meta:
        model = CustomerMetadata
        fields = ('first_name', 'last_name', 'date_of_birth', 'phone_number')
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Ensure required fields for customer_id generation are provided
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        date_of_birth = cleaned_data.get('date_of_birth')
        
        if not first_name:
            self.add_error('first_name', 'First name is required for customer metadata')
        
        if not last_name:
            self.add_error('last_name', 'Last name is required for customer metadata')
        
        if not date_of_birth:
            self.add_error('date_of_birth', 'Date of birth is required for customer metadata')
        
        return cleaned_data


class BookmarkProductForm(forms.ModelForm):
    """
    Form for bookmarking a product.
    """
    class Meta:
        model = BookmarkedProduct
        fields = ('product_id',)


class ViewProductForm(forms.ModelForm):
    """
    Form for recording a product view.
    """
    class Meta:
        model = ViewHistory
        fields = ('product_id', 'product_category', 'product_company')