from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.password_validation import validate_password
from assets.models import CustomUser, Category, Tag, Asset, Department, Profile, AssetAssignment

# ====================== Custom User Serializer =======================
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'firstName', 'lastName', 'date_joined']

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
    assignedTo = UserSerializer()

    class Meta:
        model = Asset
        fields = [
            'id', 'name', 'assetType', 'description',
            'serialNumber', 'category', 'tags', 'assignedTo', 
            'assignedDepartment'
        ]

# ========================== USER MANAGEMENT SERIALIZERS MODULES =============================
# Serializer for user registration
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['firstName', 'lastName', 'email', 'username', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create(
            firstName=validated_data['firstName'],
            lastName=validated_data['lastName'],
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
class LoginSerializer(serializers.Serializer):
    usernameOrEmail = serializers.CharField()
    password = serializers.CharField(write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, attrs):
        usernameOrEmail = attrs.get('usernameOrEmail')
        password = attrs.get('password')

        if not usernameOrEmail or not password:
            raise serializers.ValidationError("Username/Email and password are required")

        # Try to authenticate with the username_or_email as username first
        user = authenticate(username=usernameOrEmail, password=password)

        if user is None:
            # If authentication with username fails, try with email
            try:
                user_obj = CustomUser.objects.get(email=usernameOrEmail)  # Use CustomUser instead of User
                user = authenticate(username=user_obj.username, password=password)
            except CustomUser.DoesNotExist:  # Use CustomUser instead of User
                raise serializers.ValidationError("Invalid login credentials")

        if user is None:
            raise serializers.ValidationError("Invalid login credentials")

        refresh = RefreshToken.for_user(user)
        attrs['refresh'] = str(refresh)
        attrs['access'] = str(refresh.access_token)
        attrs['user'] = user

        return attrs

# ===================== User Changing password ===============================
class PasswordChangeSerializer(serializers.Serializer):
    oldPassword = serializers.CharField(write_only=True)
    newPassword = serializers.CharField(write_only=True)
    newPasswordConfirm = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['newPassword'] != data['newPasswordConfirm']:
            raise serializers.ValidationError("New passwords do not match")
        return data

    def validate_oldPassword(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect")
        return value

# ================= Reseting user password by sending reset token to email =================
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("There is no user registered with this email address.")
        return value
# ================ Confirm password reset =============================

from rest_framework import serializers

class PasswordResetConfirmSerializer(serializers.Serializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(max_length=128, write_only=True)
    confirm_new_password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        confirm_new_password = attrs.get('confirm_new_password')

        if new_password != confirm_new_password:
            raise serializers.ValidationError("Passwords do not match.")
        
        return attrs
# ==================== User Profile ======================
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['name']

class ProfileSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'user', 'department', 'role']
        read_only_fields = ['user', 'department', 'role']

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'firstName', 'lastName', 'date_joined']
        extra_kwargs = {
            'username': {'required': False},
            'email': {'required': False},
        }

class ProfileUpdateSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(partial=True)  # Allow partial updates on user
    department = DepartmentSerializer()

    class Meta:
        model = Profile
        fields = ['user', 'department', 'role']

    def validate(self, data):
        """
        Validate username and email uniqueness if provided.
        """
        user_data = data.get('user', {})
        username = user_data.get('username', None)
        email = user_data.get('email', None)

        # Check for unique username
        if username:
            if CustomUser.objects.exclude(id=self.instance.user.id).filter(username=username).exists():
                raise serializers.ValidationError({
                    'user': {
                        'username': 'A user with that username already exists.'
                    }
                })

        # Check for unique email
        if email:
            if CustomUser.objects.exclude(id=self.instance.user.id).filter(email=email).exists():
                raise serializers.ValidationError({
                    'user': {
                        'email': 'A user with this email already exists.'
                    }
                })

        return data

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        department_data = validated_data.pop('department', None)

        # Update Profile fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if user_data:
            user = instance.user
            for attr, value in user_data.items():
                if value is not None:  # Only update if value is provided
                    setattr(user, attr, value)
            user.save()

        if department_data:
            department, created = Department.objects.get_or_create(**department_data)
            instance.department = department

        instance.save()
        return instance

# ===================== Asset Assignment ======================
class AssetAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetAssignment
        fields = ['id', 'asset', 'user', 'assignedTo', 'assignedDepartment', 'returnDate']

# ===================== Asset With Category =================
class AssetWithCategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Asset
        fields = '__all__'
