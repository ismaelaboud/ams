from django.contrib.auth.models import AbstractUser
from django.db import models

# Custom User model extending AbstractUser
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, max_length=50)  # Unique email field for the user
    firstName = models.CharField(max_length=30)  # First name of the user
    lastName = models.CharField(max_length=30)  # Last name of the user
    
    # Many-to-many relationship with groups, with a custom related_name to avoid clashes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customUserGroups',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    
    # Many-to-many relationship with user permissions, with a custom related_name to avoid clashes
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customUserPermissions',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )

    def __str__(self):
        return self.username  # Return username as string representation


class Department(models.Model):
    id = models.AutoField(primary_key=True)  # Unique identifier for the department
    name = models.CharField(max_length=50)  # Department name

    def __str__(self):
        return self.name  # Return department name

    class Meta:
        db_table = 'departments'  # Table name for Department model


class Profile(models.Model):
    USER_ROLE = 'USER'
    ADMIN_ROLE = 'ADMIN'
    
    ROLE_CHOICES = [
        (USER_ROLE, 'User'),
        (ADMIN_ROLE, 'Admin'),
    ]

    id = models.AutoField(primary_key=True)  # Unique identifier for the profile
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)  # One-to-one relationship with CustomUser
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default=USER_ROLE)  # Role of the user
    department = models.ForeignKey(Department, on_delete=models.CASCADE)  # Department of the user

    def __str__(self):
        return self.user.username  # Return username of associated user

    class Meta:
        db_table = 'profiles'  # Table name for Profile model


class Category(models.Model):
    id = models.AutoField(primary_key=True)  # Unique identifier for the category
    name = models.CharField(max_length=50)  # Name of the category

    def __str__(self):
        return self.name  # Return category name

    class Meta:
        db_table = 'categories'  # Table name for Category model


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)  # Name of the tag

    def __str__(self):
        return self.name  # Return tag name

    class Meta:
        db_table = 'tags'  # Table name for Tag model
class Asset(models.Model):
    id = models.AutoField(primary_key=True)  # Unique identifier for the asset
    name = models.CharField(max_length=50)  # Name of the asset
    assetType = models.CharField(max_length=50)  # Type of the asset
    description = models.TextField()  # Description of the asset
    serialNumber = models.CharField(max_length=255, unique=True)  # Unique serial number of the asset
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Category foreign key
    assignedDepartment = models.ForeignKey(Department, on_delete=models.CASCADE)  # Department to which the asset is assigned
    dateRecorded = models.DateTimeField(auto_now_add=True)  # Timestamp when the asset was recorded
    status = models.BooleanField(default=True)  # Status of the asset (active/inactive)
    tags = models.ManyToManyField(Tag, through='AssetTag')  # Many-to-many relationship with tags

    def __str__(self):
        return self.name  # Return asset name

    class Meta:
        db_table = 'assets'  # Table name for Asset model


class AssetTag(models.Model):
    id = models.AutoField(primary_key=True)  # Unique identifier for the AssetTag
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)  # Foreign key to Asset
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)  # Foreign key to Tag

    class Meta:
        db_table = 'asset_tags'  # Table name for AssetTag model
        unique_together = ('asset', 'tag')  # Ensure unique asset-tag pairs


class AssetAssignment(models.Model):
    id = models.AutoField(primary_key=True)  # Unique identifier for the asset assignment
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)  # Asset being assigned
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # User assigned to the asset
    assignedTo = models.ForeignKey(Profile, on_delete=models.CASCADE)  # Profile of the user assigned to the asset
    assignedDepartment = models.ForeignKey(Department, on_delete=models.CASCADE)  # Department to which the asset is assigned
    dateAssigned = models.DateField(auto_now_add=True)  # Date when the asset was assigned
    returnDate = models.DateField(null=True, blank=True)  # Expected return date

    def __str__(self):
        return f"{self.asset.name} assigned to {self.assignedTo.user.username}"

    class Meta:
        db_table = 'asset_assignments'  # Table name for AssetAssignment model
