from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from .models import CustomerMetadata
from .forms import CustomerRegistrationForm

@csrf_protect
def customer_register(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            # Create CustomerMetadata object but don't save it yet
            customer = form.save(commit=False)
            
            # If customer_id is not provided, it will be auto-generated in the save method
            customer.save()
            
            messages.success(request, 'Registration successful! Your customer ID is: {}'.format(customer.customer_id))
            return redirect('registration_success')  # Redirect to success page
    else:
        form = CustomerRegistrationForm()
    
    return render(request, 'customer_registration.html', {'form': form})

def registration_success(request):
    return render(request, 'registration_success.html')