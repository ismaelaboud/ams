from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.password_validation import validate_password
from assets.models import CustomUser, Category, Tag, Asset


# Serializer for user registration
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'password2', 'email', 'firstName', 'lastName']
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
            'firstName': {'required': True},
            'lastName': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['firstName'],
            last_name=validated_data['lastName']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

# Serializer for user login
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if not username or not password:
            raise serializers.ValidationError("Username and password are required")

        try:
            user = CustomUser.objects.get(username=username)
            if not user.check_password(password):
                raise serializers.ValidationError("Incorrect password")
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("User does not exist")

        refresh = RefreshToken.for_user(user)
        attrs['refresh'] = str(refresh)
        attrs['access'] = str(refresh.access_token)

        return attrs

class PasswordResetSerializer(serializers.Serializer):
    oldPassword = serializers.CharField(write_only=True)
    newPassword = serializers.CharField(write_only=True)
    newPasswordConfirm = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['newPassword'] != data['newPasswordConfirm']:
            raise serializers.ValidationError("New passwords do not match")
        return data

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect")
        return value

    def validate_new_password(self, value):
        validate_password(value)
        return value
    

# Serializer for the CustomUser model
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email']

# Serializer for the Category model
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

# Serializer for the Tag model
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

# Serializer for the Asset model
class AssetSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    tags = TagSerializer(many=True)
    from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.password_validation import validate_password
from assets.models import CustomUser, Category, Tag, Asset


# Serializer for user registration
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'password2', 'email', 'firstName', 'lastName']
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
            'firstName': {'required': True},
            'lastName': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['firstName'],
            last_name=validated_data['lastName']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

# Serializer for user login
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if not username or not password:
            raise serializers.ValidationError("Username and password are required")

        try:
            user = CustomUser.objects.get(username=username)
            if not user.check_password(password):
                raise serializers.ValidationError("Incorrect password")
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("User does not exist")

        refresh = RefreshToken.for_user(user)
        attrs['refresh'] = str(refresh)
        attrs['access'] = str(refresh.access_token)

        return attrs

class PasswordResetSerializer(serializers.Serializer):
    oldPassword = serializers.CharField(write_only=True)
    newPassword = serializers.CharField(write_only=True)
    newPasswordConfirm = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['newPassword'] != data['newPasswordConfirm']:
            raise serializers.ValidationError("New passwords do not match")
        return data

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect")
        return value

    def validate_new_password(self, value):
        validate_password(value)
        return value
    

# Serializer for the CustomUser model
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email']

# Serializer for the Category model
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

# Serializer for the Tag model
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

# Serializer for the Asset model
class AssetSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    tags = TagSerializer(many=True)

    class Meta:
        model = Asset
        fields = [
            'id', 'name', 'assetType', 'description',
            'serialNumber', 'category', 'tags', 
            'assignedDepartment'
        ]


    class Meta:
        model = Asset
        fields = [
            'id', 'name', 'assetType', 'description',
            'serialNumber', 'category', 'tags', 
            'assignedDepartment'
        ]
