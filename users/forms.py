from django import forms
from .models import User  # Adjust import if needed

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'date_of_birth', 'mobile_number', 'email', 'password']
