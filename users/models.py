from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)

        # Only generate username if not provided
        if 'username' not in extra_fields or not extra_fields['username']:
            if all(field in extra_fields for field in ['first_name', 'last_name', 'date_of_birth']):
                extra_fields['username'] = self.generate_username(
                    extra_fields['first_name'],
                    extra_fields['last_name'],
                    extra_fields['date_of_birth']
                )
            else:
                raise ValueError("first_name, last_name, and date_of_birth are required for customer username generation")

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        # Ensure superuser provides a username manually
        if 'username' not in extra_fields or not extra_fields['username']:
            raise ValueError("Superusers must have a username explicitly defined.")

        return self.create_user(email, password, **extra_fields)

    def generate_username(self, first_name, last_name, dob):
        dob_str = dob.strftime('%Y%m%d')
        return f"{first_name[:3].lower()}{last_name[:3].lower()}{dob_str}"

class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    mobile_number = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=20, unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'date_of_birth', 'mobile_number']

    def __str__(self):
        return self.username
