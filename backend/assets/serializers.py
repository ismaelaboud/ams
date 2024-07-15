# serializers.py
from rest_framework import serializers
from assets.models import CustomUser as User, Category, Tag, Asset

# ==== SERIALIZATION INVOLVES CONVERTING DATA INTO JSON FORMAT WHICH IS BASICALLY, CREATING API ==========

# Serializer for the CustomUser model
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User  # Model to be serialized
        fields = ['id', 'username', 'email']  # Fields to include in the serialized output


# Serializer for the Category model
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category  # Model to be serialized
        fields = ['id', 'name']  # Fields to include in the serialized output


# Serializer for the Tag model
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag  # Model to be serialized
        fields = ['id', 'name']  # Fields to include in the serialized output


# Serializer for the Asset model
class AssetSerializer(serializers.ModelSerializer):
    # Nested serializer to include category details within the asset
    category = CategorySerializer()
    # Nested serializer to include multiple tag details within the asset
    tags = TagSerializer(many=True)
    # Nested serializer to include user details of the user assigned to the asset
    assigned_to = UserSerializer()

    class Meta:
        model = Asset  # Model to be serialized
        fields = ['id', 'name', 'asset_type', 'description', 'serial_number', 'category', 'tags', 'assigned_to', 'assigned_department']  # Fields to include in the serialized output
