from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.apps import apps
from .models import User
from .serializers import (
    UserSerializer, 
    ProductViewSerializer, 
    BookmarkProductSerializer,
    StoreCustomerLinkSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for the User model."""
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Ensure users can only see their own profile unless they're staff."""
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)
    
    @action(detail=True, methods=['get'])
    def view_history(self, request, pk=None):
        """Get a user's product view history."""
        user = self.get_object()
        ProductView = apps.get_model('store', 'ProductView')
        
        views = ProductView.objects.filter(user=user).select_related('product')
        
        data = [
            {
                'product_id': view.product.id,
                'product_name': view.product.name,
                'viewed_at': view.viewed_at
            }
            for view in views
        ]
        
        return Response(data)
    
    @action(detail=True, methods=['get'])
    def bookmarks(self, request, pk=None):
        """Get a user's bookmarked products."""
        user = self.get_object()
        Products = apps.get_model('store', 'Products')
        
        bookmarks = Products.objects.filter(bookmarked_by_users=user)
        
        return Response({
            "count": bookmarks.count(),
            "results": [
                {"id": product.id, "name": product.name}
                for product in bookmarks
            ]
        })
    
    @action(detail=True, methods=['post'])
    def add_bookmark(self, request, pk=None):
        """Add a product to user's bookmarks."""
        user = self.get_object()
        serializer = BookmarkProductSerializer(data=request.data)
        
        if serializer.is_valid():
            product_id = serializer.validated_data['product_id']
            Products = apps.get_model('store', 'Products')
            
            try:
                product = Products.objects.get(id=product_id)
                user.bookmark_product(product)
                return Response({"status": "Product added to bookmarks"}, status=status.HTTP_200_OK)
            except Products.DoesNotExist:
                return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def remove_bookmark(self, request, pk=None):
        """Remove a product from user's bookmarks."""
        user = self.get_object()
        serializer = BookmarkProductSerializer(data=request.data)
        
        if serializer.is_valid():
            product_id = serializer.validated_data['product_id']
            Products = apps.get_model('store', 'Products')
            
            try:
                product = Products.objects.get(id=product_id)
                user.remove_bookmark(product)
                return Response({"status": "Product removed from bookmarks"}, status=status.HTTP_200_OK)
            except Products.DoesNotExist:
                return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def record_view(self, request, pk=None):
        """Record a product view in user's history."""
        user = self.get_object()
        serializer = BookmarkProductSerializer(data=request.data)
        
        if serializer.is_valid():
            product_id = serializer.validated_data['product_id']
            Products = apps.get_model('store', 'Products')
            
            try:
                product = Products.objects.get(id=product_id)
                user.record_product_view(product)
                return Response({"status": "Product view recorded"}, status=status.HTTP_201_CREATED)
            except Products.DoesNotExist:
                return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def link_store_customer(self, request, pk=None):
        """Link this user to an existing store.Customers record."""
        user = self.get_object()
        serializer = StoreCustomerLinkSerializer(data=request.data)
        
        if serializer.is_valid():
            customer_id = serializer.validated_data['customer_id']
            Customers = apps.get_model('store', 'Customers')
            
            try:
                # Check if the customer is already linked
                if hasattr(user, 'store_customer_profile') and user.store_customer_profile:
                    return Response(
                        {"error": "User already linked to a customer record"}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                store_customer = Customers.objects.get(id=customer_id)
                
                # Check if this customer is already linked to another user
                if store_customer.user and store_customer.user != user:
                    return Response(
                        {"error": "This customer is already linked to another user"}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                user.link_store_customer(store_customer)
                return Response({"status": "Customer record linked successfully"}, status=status.HTTP_200_OK)
            except Customers.DoesNotExist:
                return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)