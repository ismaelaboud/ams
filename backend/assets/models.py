from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_migrate
from django.dispatch import receiver

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
<<<<<<< HEAD
        db_table = 'profile'  # Table name for Profile model
=======
        db_table = 'profiles'
>>>>>>> backend


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
<<<<<<< HEAD
        db_table = 'categorie'  # Table name for Category model
=======
        db_table = 'categories'


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
>>>>>>> backend


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
<<<<<<< HEAD
        db_table = 'tag'  # Table name for Tag model
=======
        db_table = 'tags'


>>>>>>> backend
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
<<<<<<< HEAD
        db_table = 'asset'  # Table name for Asset model
=======
        db_table = 'assets'
>>>>>>> backend


class AssetTag(models.Model):
    id = models.AutoField(primary_key=True)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
<<<<<<< HEAD
        db_table = 'assetTag'  # Table name for AssetTag model
        unique_together = ('asset', 'tag')  # Ensure unique asset-tag pairs
=======
        db_table = 'asset_tags'
        unique_together = ('asset', 'tag')
>>>>>>> backend


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
<<<<<<< HEAD
        db_table = 'assetAssignment'  # Table name for AssetAssignment model
=======
        db_table = 'asset_assignments'
>>>>>>> backend
