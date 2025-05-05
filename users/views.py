from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import F, Count, Max
from django.utils import timezone
from django.contrib.auth.models import User

from .models import CustomerMetadata, BookmarkedProduct, ViewHistory
from .serializers import (
    CustomerMetadataSerializer, BookmarkedProductSerializer, 
    ViewHistorySerializer, CustomerHistorySerializer
)


class CustomerMetadataViewSet(viewsets.ModelViewSet):
    """
    API endpoint for CustomerMetadata model operations.
    """
    queryset = CustomerMetadata.objects.all()
    serializer_class = CustomerMetadataSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Filter queryset based on user permissions.
        Regular users can only see their own data.
        Staff users can see all customer metadata.
        """
        user = self.request.user
        if user.is_staff:
            return CustomerMetadata.objects.all()
        try:
            return CustomerMetadata.objects.filter(user=user)
        except CustomerMetadata.DoesNotExist:
            return CustomerMetadata.objects.none()
    
    @action(detail=True, methods=['get'])
    def bookmarks(self, request, pk=None):
        """List all bookmarked products for a customer."""
        customer = self.get_object()
        bookmarks = BookmarkedProduct.objects.filter(customer=customer)
        serializer = BookmarkedProductSerializer(bookmarks, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def view_history(self, request, pk=None):
        """List the view history for a customer."""
        customer = self.get_object()
        history = ViewHistory.objects.filter(customer=customer).order_by('-viewed_at')
        serializer = ViewHistorySerializer(history, many=True)
        return Response(serializer.data)


class BookmarkedProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint for BookmarkedProduct model operations.
    """
    queryset = BookmarkedProduct.objects.all()
    serializer_class = BookmarkedProductSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Filter queryset based on user permissions.
        Regular users can only see their own bookmarks.
        Staff users can see all bookmarks.
        """
        user = self.request.user
        if user.is_staff:
            return BookmarkedProduct.objects.all()
        try:
            customer = CustomerMetadata.objects.get(user=user)
            return BookmarkedProduct.objects.filter(customer=customer)
        except CustomerMetadata.DoesNotExist:
            return BookmarkedProduct.objects.none()
    
    def create(self, request, *args, **kwargs):
        """
        Create a bookmark.
        If the customer is not specified, use the current authenticated user's metadata.
        """
        if not request.data.get('customer'):
            try:
                customer = CustomerMetadata.objects.get(user=request.user)
                request.data['customer'] = customer.id
            except CustomerMetadata.DoesNotExist:
                return Response(
                    {"error": "No customer metadata found for current user."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
        return super().create(request, *args, **kwargs)


class ViewHistoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint for ViewHistory model operations.
    """
    queryset = ViewHistory.objects.all()
    serializer_class = ViewHistorySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Filter queryset based on user permissions.
        Regular users can only see their own view history.
        Staff users can see all view histories.
        """
        user = self.request.user
        if user.is_staff:
            return ViewHistory.objects.all()
        try:
            customer = CustomerMetadata.objects.get(user=user)
            return ViewHistory.objects.filter(customer=customer)
        except CustomerMetadata.DoesNotExist:
            return ViewHistory.objects.none()
    
    def create(self, request, *args, **kwargs):
        """
        Record a product view.
        If the customer is not specified, use the current authenticated user's metadata.
        If the product has been viewed before, increment the view count.
        """
        if not request.data.get('customer'):
            try:
                customer = CustomerMetadata.objects.get(user=request.user)
                request.data['customer'] = customer.id
            except CustomerMetadata.DoesNotExist:
                return Response(
                    {"error": "No customer metadata found for current user."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
        # Check if the product is already in view history
        customer_id = request.data.get('customer')
        product_id = request.data.get('product_id')
        
        try:
            # Try to get an existing view history record
            view_history = ViewHistory.objects.get(
                customer_id=customer_id,
                product_id=product_id
            )
            
            # Update the view count and viewed_at timestamp
            view_history.view_count = F('view_count') + 1
            
            # Update category and company if provided
            if 'product_category' in request.data:
                view_history.product_category = request.data['product_category']
            if 'product_company' in request.data:
                view_history.product_company = request.data['product_company']
                
            view_history.viewed_at = timezone.now()
            view_history.save()
            
            # Refresh the instance to get the new value of F() expressions
            view_history.refresh_from_db()
            
            serializer = self.get_serializer(view_history)
            return Response(serializer.data)
            
        except ViewHistory.DoesNotExist:
            # Create a new view history record
            return super().create(request, *args, **kwargs)


class CustomerHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only API endpoint for aggregated customer history.
    Shows most viewed categories, companies, etc.
    """
    serializer_class = CustomerHistorySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Return aggregated statistics for customers.
        """
        user = self.request.user
        
        # Base query - get all customers with their metadata
        if user.is_staff:
            customers = CustomerMetadata.objects.all()
        else:
            try:
                customers = CustomerMetadata.objects.filter(user=user)
            except CustomerMetadata.DoesNotExist:
                customers = CustomerMetadata.objects.none()
        
        result = []
        
        # For each customer, gather aggregated stats
        for customer in customers:
            # Get most viewed category
            top_category = ViewHistory.objects.filter(
                customer=customer
            ).values('product_category').annotate(
                count=Count('id')
            ).order_by('-count').first()
            
            # Get most viewed company
            top_company = ViewHistory.objects.filter(
                customer=customer
            ).values('product_company').annotate(
                count=Count('id')
            ).order_by('-count').first()
            
            # Count total unique products viewed
            total_products = ViewHistory.objects.filter(
                customer=customer
            ).values('product_id').distinct().count()
            
            # Count bookmarks
            bookmark_count = BookmarkedProduct.objects.filter(
                customer=customer
            ).count()
            
            result.append({
                'customer_id': customer.customer_id,
                'most_viewed_category': top_category['product_category'] if top_category else '-',
                'most_viewed_company': top_company['product_company'] if top_company else '-',
                'total_products_viewed': total_products,
                'bookmark_count': bookmark_count
            })
        
        return result