from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator

class UserCredManager(BaseUserManager):
    """Manager for the custom UserCred model."""
    
    def create_user(self, email, user_name=None, password=None, **extra_fields):
        """Create and save a regular user with the given email and password."""
        if not email:
            raise ValueError('The Email field must be set')
        
        email = self.normalize_email(email)
        user = self.model(user_email=email, user_name=user_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, user_name=None, password=None, **extra_fields):
        """Create and save a superuser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, user_name, password, **extra_fields)

class UserCred(AbstractBaseUser, PermissionsMixin):
    """Custom user model that uses email as the primary identifier."""
    
    user_name = models.CharField(max_length=50, blank=True, null=True, unique=True)
    user_email = models.EmailField(_('email address'), unique=True)
    user_phone_no = models.CharField(max_length=10, blank=True)
    user_pass = models.CharField(max_length=200, blank=True, null=True)
    
    # Profile picture field (optional)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/', 
        blank=True, 
        null=True, 
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )

    # Add fields for user status
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Designates whether the user can log into the admin site.

    # Define the manager for this model
    objects = UserCredManager()

    USERNAME_FIELD = 'user_email'  # Use email as the unique identifier for login
    REQUIRED_FIELDS = ['user_name']  # Fields required when creating a user via CLI (manage.py createsuperuser)

    def __str__(self):
        return self.user_email
