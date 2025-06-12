from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from datetime import datetime

from .models import CustomerMetadata, BookmarkedProduct, ViewHistory


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the default Django User model."""
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        read_only_fields = ('id', 'username')


class CustomerMetadataSerializer(serializers.ModelSerializer):
    """Serializer for the CustomerMetadata model."""
    date_of_birth = serializers.DateField(
        input_formats=['%d-%m-%Y'],
        required=False
    )
    user = UserSerializer(read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = CustomerMetadata
        fields = (
            'id', 'user', 'username', 'email', 'first_name', 'last_name',
            'date_of_birth', 'customer_id', 'phone_number'
        )
        read_only_fields = ('customer_id', 'user')
    
    def validate(self, data):
        """
        Custom validation to ensure all required fields for customer_id
        generation are provided when updating CustomerMetadata.
        """
        if not data.get('first_name') and not self.instance.first_name:
            raise ValidationError("First name is required for customer creation")
        if not data.get('last_name') and not self.instance.last_name:
            raise ValidationError("Last name is required for customer creation")
        if not data.get('date_of_birth') and not self.instance.date_of_birth:
            raise ValidationError("Date of birth is required for customer creation")
        
        return data


class BookmarkedProductSerializer(serializers.ModelSerializer):
    """Serializer for the BookmarkedProduct model."""
    customer_id = serializers.CharField(source='customer.customer_id', read_only=True)
    
    class Meta:
        model = BookmarkedProduct
        fields = ('id', 'customer', 'customer_id', 'product_id', 'bookmarked_at')
        read_only_fields = ('bookmarked_at',)


class ViewHistorySerializer(serializers.ModelSerializer):
    """Serializer for the ViewHistory model."""
    customer_id = serializers.CharField(source='customer.customer_id', read_only=True)
    
    class Meta:
        model = ViewHistory
        fields = ('id', 'customer', 'customer_id', 'product_id', 'product_category', 
                 'product_company', 'viewed_at', 'view_count')
        read_only_fields = ('viewed_at',)


class CustomerHistorySerializer(serializers.Serializer):
    """Serializer for aggregated customer history."""
    customer_id = serializers.CharField()
    most_viewed_category = serializers.CharField()
    most_viewed_company = serializers.CharField()
    total_products_viewed = serializers.IntegerField()
    bookmark_count = serializers.IntegerField()