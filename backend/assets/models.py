from django.db import models
from django.contrib.auth.models import AbstractUser # Custom user model extending AbstractUser
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .barcode_gen import generate_barcode
from django.core.files import File
import os
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, max_length=50)  # Unique email field
    firstName = models.CharField(max_length=30)  # First name field
    lastName = models.CharField(max_length=30)  # Last name field
    
    # Many-to-many field for user groups
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customUserGroups',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    
    # Many-to-many field for user permissions
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customUserPermissions',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )

    def __str__(self):
        return self.username  # String representation of the user


# Model representing a department
class Department(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    name = models.CharField(max_length=50, unique=True)  # Name of the department

    def __str__(self):
        return self.name  # String representation of the department

    class Meta:
        db_table = 'departments'  # Custom database table name


# Signal receiver to create default departments after migrations
@receiver(post_migrate)
def create_default_departments(sender, **kwargs):
    if sender.name == 'assets':  # Check if the sender app is 'assets'
        default_departments = [
            'Technology',
            'Communication',
            'Heritage',
            'Creative',
            'Case management',
            'Community',
            'Green Economy',
            'Entrepreneurship',
            'Engineering',
        ]
        # Create each default department if it doesn't exist
        for department_name in default_departments:
            Department.objects.get_or_create(name=department_name)


# Model representing a user profile
class Profile(models.Model):
    USER_ROLE = 'USER'
    ADMIN_ROLE = 'ADMIN'
    
    ROLE_CHOICES = [
        (USER_ROLE, 'User'),
        (ADMIN_ROLE, 'Admin'),
    ]

    id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)  # One-to-one relationship with CustomUser
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default=USER_ROLE)  # Role field with choices
    department = models.ForeignKey(Department, on_delete=models.SET_DEFAULT, default=1)  # Set a default department ID
  # Foreign key to Department

    def __str__(self):
        return self.user.username  # String representation of the profile

    class Meta:
        db_table = 'profiles'  # Custom database table name


# Model representing a category
class Category(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    name = models.CharField(max_length=50)  # Name of the category

    def __str__(self):
        return self.name  # String representation of the category

    class Meta:
        db_table = 'categories'  # Custom database table name


# Signal receiver to create default categories after migrations
@receiver(post_migrate)
def create_default_categories(sender, **kwargs):
    if sender.name == 'assets':  # Check if the sender app is 'assets'
        default_categories = [
            'Furnitures',
            'Electronics',
            'Office Supplies',
        ]
        # Create each default category if it doesn't exist
        for category_name in default_categories:
            Category.objects.get_or_create(name=category_name)


# Model representing a tag
class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    barcode_image = models.ImageField(upload_to='barcodes/', blank=True, null=True)
    barcode_number = models.CharField(max_length=13,unique=True, blank=True, null=True)

    def __str__(self):
        return self.name  # String representation of the tag

    def save(self, *args, **kwargs):
        if not self.barcode_image:
            # Generate the barcode
            barcode_path, barcode_number = generate_barcode(self.name)
            
            # Save the barcode image
            with open(barcode_path, 'rb') as f:
                self.barcode_image.save(os.path.basename(barcode_path), File(f), save=False)
            
            # Save the barcode number
            self.barcode_number = barcode_number
        
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'tags'  # Custom database table name


# Model representing an asset
class Asset(models.Model):
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Booked', 'Booked'),
        ('Maintenance', 'Maintenance'),
        ('In use', 'In use'),
        ('Archived', 'Archived'),
    ]

    id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    name = models.CharField(max_length=50)  # Name of the asset
    assetType = models.CharField(max_length=50)  # Type of the asset
    description = models.TextField()  # Description of the asset
    serialNumber = models.CharField(max_length=255, unique=True)  # Unique serial number
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Foreign key to Category
    assignedDepartment = models.ForeignKey(Department, on_delete=models.CASCADE)  # Foreign key to Department
    dateRecorded = models.DateTimeField(auto_now_add=True)  # Date the asset was recorded
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')  # Status of the asset

    def __str__(self):
        return self.name  # String representation of the asset

    class Meta:
        db_table = 'assets'  # Custom database table name


# Model representing an asset tag relationship
class AssetTag(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)  # Foreign key to Asset
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)  # Foreign key to Tag

    class Meta:
        db_table = 'asset_tags'  # Custom database table name
        unique_together = ('asset', 'tag')  # Unique constraint for asset and tag


# Model representing an asset assignment
class AssetAssignment(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)  # Foreign key to Asset
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Foreign key to CustomUser
    assignedTo = models.ForeignKey(Profile, on_delete=models.CASCADE)  # Foreign key to Profile
    assignedDepartment = models.ForeignKey(Department, on_delete=models.CASCADE)  # Foreign key to Department
    dateAssigned = models.DateField(auto_now_add=True)  # Date the asset was assigned
    returnDate = models.DateField(null=True, blank=True)  # Optional return date

    def __str__(self):
        return f"{self.asset.name} assigned to {self.assignedTo.user.username}"  # String representation of the assignment

    class Meta:
        db_table = 'assetAssignment'  # Custom database table name
