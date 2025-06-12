from django import forms
from django.utils.translation import gettext_lazy as _
from .models import CustomerMetadata

class CustomerRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput,
        max_length=100,
        help_text=_('Enter a secure password')
    )
    
    confirm_password = forms.CharField(
        label=_('Confirm Password'),
        widget=forms.PasswordInput,
        max_length=100,
        help_text=_('Enter the same password as before')
    )
    
    class Meta:
        model = CustomerMetadata
        fields = ['first_name', 'last_name', 'customer_id', 'date_of_birth', 'email', 'password']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'customer_id': forms.TextInput(attrs={'placeholder': 'Leave blank to auto-generate'}),
        }
        help_texts = {
            'customer_id': _('Optional: 12 character alphanumeric ID or leave blank to auto-generate'),
            'date_of_birth': _('Format: YYYY-MM-DD'),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', _('Passwords do not match'))
        
        return cleaned_data