from django.contrib.auth.models import AbstractUser
from django.db import models

# Custom User model extending AbstractUser
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # Unique email field for the user
    first_name = models.CharField(max_length=150)  # First name of the user
    last_name = models.CharField(max_length=150)  # Last name of the user
    
    # Many-to-many relationship with groups, with a custom related_name to avoid clashes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    
    # Many-to-many relationship with user permissions, with a custom related_name to avoid clashes
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )

    def __str__(self):
        return self.username  # Return username as string representation
