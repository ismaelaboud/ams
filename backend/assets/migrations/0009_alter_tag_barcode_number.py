# Generated by Django 5.0.6 on 2024-07-23 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0008_tag_barcode_image_tag_barcode_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='barcode_number',
            field=models.CharField(blank=True, max_length=13, null=True, unique=True),
        ),
    ]
