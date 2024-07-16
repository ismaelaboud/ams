# assets/admin.py

from django.contrib import admin
from .models import CustomUser, Asset, Category, Tag, Department, AssetAssignment, Profile, AssetTag

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Asset)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Department)
admin.site.register(AssetAssignment)
admin.site.register(Profile)
admin.site.register(AssetTag)
