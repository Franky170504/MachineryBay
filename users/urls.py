from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.views.generic import TemplateView
from . import forms
from . import views

# Create a router and register our viewsets
# router = DefaultRouter()
# router.register(r'metadata', views.CustomerMetadataViewSet)
# router.register(r'bookmarks', views.BookmarkedProductViewSet)
# router.register(r'view-history', views.ViewHistoryViewSet)
# router.register(r'customer-history', views.CustomerHistoryViewSet, basename='customer-history')

app_name = "users"
# The API URLs are determined automatically by the router
urlpatterns = [
    path("register/", views.customer_register, name='customer_register'),
    path("register/success/", views.registration_success, name='registration_success'),
    # path("", include(router.urls)),
]