# Generated by Django 5.0.6 on 2024-07-19 17:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0006_alter_assetassignment_table_alter_category_table'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='category',
            table='categories',
        ),
    ]
