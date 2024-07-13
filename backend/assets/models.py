from django.contrib.auth.models import AbstractUser
from django.db import models

# Custom User model extending AbstractUser
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # Unique email field for the user
    firstName = models.CharField(max_length=150)  # First name of the user
    lastName = models.CharField(max_length=150)  # Last name of the user
    
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


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)  # One-to-one relationship with CustomUser
    role = models.CharField(max_length=255)  # Role of the user (e.g., 'admin', 'user')
    department = models.ForeignKey('Department', on_delete=models.CASCADE)  # Department of the user

    def __str__(self):
        return self.user.username  # Return username of associated user

    class Meta:
        db_table = 'profiles'  # Table name for Profile model


# Department model for asset departments
class Department(models.Model):
    name = models.CharField(max_length=255)  # Department name

    def __str__(self):
        return self.name  # Return department name

    class Meta:
        db_table = 'departments'  # Table name for Department model


# Category model for asset categorization
class Category(models.Model):
    name = models.CharField(max_length=255)  # Name of the category

    def __str__(self):
        return self.name  # Return category name

    class Meta:
        db_table = 'categories'  # Table name for Category model


# Tag model for asset tagging
class Tag(models.Model):
    name = models.CharField(max_length=255)  # Name of the tag

    def __str__(self):
        return self.name  # Return tag name

    class Meta:
        db_table = 'tags'  # Table name for Tag model


# Asset model representing individual assets
class Asset(models.Model):
    name = models.CharField(max_length=255)  # Name of the asset
    assetType = models.CharField(max_length=255)  # Type of the asset
    description = models.TextField()  # Description of the asset
    serialNumber = models.CharField(max_length=255, unique=True)  # Unique serial number of the asset
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Category foreign key
    assignedDepartment = models.ForeignKey(Department, on_delete=models.CASCADE)  # Department to which the asset is assigned
    dateRecorded = models.DateTimeField(auto_now_add=True)  # Timestamp when the asset was recorded
    status = models.BooleanField(default=True)  # Status of the asset (active/inactive)

    def __str__(self):
        return self.name  # Return asset name

    class Meta:
        db_table = 'assets'  # Table name for Asset model


# AssetAssignment model
class AssetAssignment(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)  # Asset being assigned
    userId = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # User assigned to the asset
    assignedToId = models.ForeignKey(Profile, on_delete=models.CASCADE)  # Profile of the user assigned to the asset
    assignedDepartmentId = models.ForeignKey(Department, on_delete=models.CASCADE)  # Department to which the asset is assigned
    dateAssigned = models.DateField()  # Date when the asset was assigned
    returnDate = models.DateField(null=True, blank=True)  # Expected return date

    def __str__(self):
        return f"{self.asset.name} assigned to {self.assignedToId.user.username}"

    class Meta:
        db_table = 'asset_assignments'  # Table name for AssetAssignment model
