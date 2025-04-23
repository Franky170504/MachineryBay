from django.shortcuts import render

def home(request):
    # products = Product.products.all()
    return render(request, 'store\home.html', {})