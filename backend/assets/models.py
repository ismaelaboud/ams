from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from django.db import models
from .barcode_gen import generate_barcode
from django.core.files import File
import os

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, max_length=50)
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customUserGroups',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customUserPermissions',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )

    def __str__(self):
        return self.username


class Department(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'departments'


@receiver(post_migrate)
def create_default_departments(sender, **kwargs):
    if sender.name == 'assets':
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
        for department_name in default_departments:
            Department.objects.get_or_create(name=department_name)


class Profile(models.Model):
    USER_ROLE = 'USER'
    ADMIN_ROLE = 'ADMIN'
    
    ROLE_CHOICES = [
        (USER_ROLE, 'User'),
        (ADMIN_ROLE, 'Admin'),
    ]

    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default=USER_ROLE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'profiles'

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'categories'  # Table name for Category model


@receiver(post_migrate)
def create_default_categories(sender, **kwargs):
    if sender.name == 'assets':
        default_categories = [
            'Furnitures',
            'Electronics',
            'Office Supplies',
        ]
        for category_name in default_categories:
            Category.objects.get_or_create(name=category_name)


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    barcode_image = models.ImageField(upload_to='barcodes/', blank=True, null=True)
    barcode_number = models.CharField(max_length=13,unique=True, blank=True, null=True)

    def __str__(self):
        return self.name

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
        db_table = 'tags'




class Asset(models.Model):
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Booked', 'Booked'),
        ('Maintenance', 'Maintenance'),
        ('In use', 'In use'),
        ('Archived', 'Archived'),
    ]

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    assetType = models.CharField(max_length=50)
    description = models.TextField()
    serialNumber = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    assignedDepartment = models.ForeignKey(Department, on_delete=models.CASCADE)
    dateRecorded = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'assets'



class AssetTag(models.Model):
    id = models.AutoField(primary_key=True)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        db_table = 'asset_tags'
        unique_together = ('asset', 'tag')



class AssetAssignment(models.Model):
    id = models.AutoField(primary_key=True)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    assignedTo = models.ForeignKey(Profile, on_delete=models.CASCADE)
    assignedDepartment = models.ForeignKey(Department, on_delete=models.CASCADE)
    dateAssigned = models.DateField(auto_now_add=True)
    returnDate = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.asset.name} assigned to {self.assignedTo.user.username}"

    class Meta:
        db_table = 'assetAssignment'  # Table name for AssetAssignment model

