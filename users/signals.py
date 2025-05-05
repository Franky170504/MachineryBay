from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import CustomerMetadata


@receiver(post_save, sender=User)
def create_customer_metadata(sender, instance, created, **kwargs):
    """
    Create CustomerMetadata record when a User is created.
    This ensures every user has associated metadata.
    """
    if created:
        # Use User's first and last name for initial metadata
        CustomerMetadata.objects.create(
            user=instance,
            first_name=instance.first_name,
            last_name=instance.last_name
        )


@receiver(post_save, sender=User)
def save_customer_metadata(sender, instance, **kwargs):
    """
    Update CustomerMetadata when User is saved.
    This keeps first name and last name in sync if they're updated on the User model.
    """
    if hasattr(instance, 'metadata'):
        # Only sync these fields if they're changed at the User level
        if instance.metadata.first_name != instance.first_name:
            instance.metadata.first_name = instance.first_name
        if instance.metadata.last_name != instance.last_name:
            instance.metadata.last_name = instance.last_name
        instance.metadata.save()


@receiver(pre_save, sender=CustomerMetadata)
def ensure_customer_id(sender, instance, **kwargs):
    """
    Ensure that a customer_id is generated for a CustomerMetadata instance
    if the required fields are present.
    """
    if not instance.customer_id and instance.first_name and instance.last_name and instance.date_of_birth:
        instance.customer_id = instance._generate_customer_id()