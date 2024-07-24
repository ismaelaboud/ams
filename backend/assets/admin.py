# assets/admin.py

from django.contrib import admin
from .models import CustomUser, Asset, Category, Tag, Department, AssetAssignment, Profile, AssetTag



from django.contrib import admin
from django.utils.html import format_html
from .models import Tag

class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'barcode_image_tag', 'barcode_number')

    def barcode_image_tag(self, obj):
        if obj.barcode_image:
            return format_html('<img src="{}" width="100" height="100" />'.format(obj.barcode_image.url))
        return "No Image"

    barcode_image_tag.short_description = 'Barcode Image'

admin.site.register(Tag, TagAdmin)





# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Asset)
admin.site.register(Category)

admin.site.register(Department)
admin.site.register(AssetAssignment)
admin.site.register(Profile)
admin.site.register(AssetTag)
