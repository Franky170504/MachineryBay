from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r'metadata', views.CustomerMetadataViewSet)
router.register(r'bookmarks', views.BookmarkedProductViewSet)
router.register(r'view-history', views.ViewHistoryViewSet)
router.register(r'customer-history', views.CustomerHistoryViewSet, basename='customer-history')

# The API URLs are determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
]