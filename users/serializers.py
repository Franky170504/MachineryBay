from rest_framework import serializers
from .models import User
from django.apps import apps

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model."""
    store_customer_id = serializers.SerializerMethodField()
    bookmarked_products_count = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'customer_id', 'first_name', 'last_name', 
            'email', 'date_of_birth', 'date_joined', 'store_customer_id',
            'bookmarked_products_count'
        ]
        read_only_fields = ['customer_id', 'date_joined', 'store_customer_id']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def get_store_customer_id(self, obj):
        try:
            return obj.store_customer_profile.id if hasattr(obj, 'store_customer_profile') else None
        except:
            return None
    
    def get_bookmarked_products_count(self, obj):
        Products = apps.get_model('store', 'Products')
        return Products.objects.filter(bookmarked_by_users=obj).count()
    
    def create(self, validated_data):
        """Create a new user with encrypted password."""
        password = validated_data.pop('password', None)
        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class ProductViewSerializer(serializers.Serializer):
    """Serializer for viewing product history."""
    
    product_id = serializers.IntegerField(read_only=True)
    product_name = serializers.CharField(read_only=True)
    viewed_at = serializers.DateTimeField(read_only=True)


class BookmarkProductSerializer(serializers.Serializer):
    """Serializer for bookmarking products."""
    
    product_id = serializers.IntegerField()


class StoreCustomerLinkSerializer(serializers.Serializer):
    """Serializer for linking to store.Customers."""
    
    customer_id = serializers.IntegerField()
    date_of_birth = serializers.CharField(required=False)