from django.contrib import admin
from .models import CustomUser, Asset, Category, Tag, Department, AssetAssignment

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Asset)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Department)
admin.site.register(AssetAssignment)
