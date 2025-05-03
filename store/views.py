from django.shortcuts import render
from .models import Products

def home(request):
    # products = Products.products.all()
    return render(request, 'store/home.html', {})#'products': products in curl brackets

def landing(request):
    return render(request, 'store/landing.html', {})