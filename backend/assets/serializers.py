import logging
from venv import logger
from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.password_validation import validate_password
from assets.models import CustomUser, Category, Tag, Asset, Department, Profile, AssetAssignment

# ====================== Custom User Serializer =======================
class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the CustomUser model to handle user data.
    """
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'firstName', 'lastName', 'date_joined']

# ========================== USER MANAGEMENT SERIALIZERS MODULES =============================

# Serializer for user registration
class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new user.
    """
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['firstName', 'lastName', 'email', 'username', 'password', 'password2']

    def validate(self, attrs):
        """
        Validate that password and password2 match and check for unique email and username.
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        if CustomUser.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "User with that email already exists."})
        
        if CustomUser.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError({"username": "User with that username already exists."})
        
        return attrs

    def create(self, validated_data):
        """
        Create a new user with the validated data.
        """
        validated_data.pop('password2')
        user = CustomUser.objects.create(
            firstName=validated_data['firstName'],
            lastName=validated_data['lastName'],
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def to_representation(self, instance):
        """
        Customize the representation of the user data, excluding the password fields.
        """
        response = super().to_representation(instance)
        response.pop('password', None)
        response.pop('password2', None)
        return response

# Serializer for user login
class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    """
    usernameOrEmail = serializers.CharField()
    password = serializers.CharField(write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, attrs):
        """
        Validate login credentials and generate JWT tokens.
        """
        usernameOrEmail = attrs.get('usernameOrEmail')
        password = attrs.get('password')

        if not usernameOrEmail or not password:
            raise serializers.ValidationError("Username/Email and password are required")

        # Try to authenticate with the usernameOrEmail as username first
        user = authenticate(username=usernameOrEmail, password=password)

        if user is None:
            # If authentication with username fails, try with email
            try:
                user_obj = CustomUser.objects.get(email=usernameOrEmail)
                user = authenticate(username=user_obj.username, password=password)
            except CustomUser.DoesNotExist:
                raise serializers.ValidationError("Invalid login credentials")

        if user is None:
            raise serializers.ValidationError("Invalid login credentials")

        refresh = RefreshToken.for_user(user)
        attrs['refresh'] = str(refresh)
        attrs['access'] = str(refresh.access_token)
        attrs['user'] = user

        return attrs

# ===================== User Changing Password ===============================
class PasswordChangeSerializer(serializers.Serializer):
    """
    Serializer for changing user password.
    """
    oldPassword = serializers.CharField(write_only=True)
    newPassword = serializers.CharField(write_only=True)
    newPasswordConfirm = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        Validate that new passwords match.
        """
        if data['newPassword'] != data['newPasswordConfirm']:
            raise serializers.ValidationError("New passwords do not match")
        return data

    def validate_oldPassword(self, value):
        """
        Validate that the old password is correct.
        """
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect")
        return value

# ================= Resetting User Password by Sending Reset Token to Email =================
class PasswordResetRequestSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset via email.
    """
    email = serializers.EmailField()

    def validate_email(self, value):
        """
        Validate that the email exists in the system.
        """
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("There is no user registered with this email address.")
        return value

# ================ Confirm Password Reset =============================
class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for confirming password reset with a token.
    """
    uidb64 = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(max_length=128, write_only=True)
    confirm_new_password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, attrs):
        """
        Validate that new passwords match.
        """
        new_password = attrs.get('new_password')
        confirm_new_password = attrs.get('confirm_new_password')

        if new_password != confirm_new_password:
            raise serializers.ValidationError("Passwords do not match.")
        
        return attrs

# ==================== User Profile ======================
class DepartmentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Department model.
    """
    class Meta:
        model = Department
        fields = ['id','name']

class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the Profile model.
    """
    department = DepartmentSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'user', 'department', 'role']
        read_only_fields = ['user', 'department', 'role']

class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer for the CustomUser model with optional fields.
    """
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'firstName', 'lastName', 'date_joined']
        extra_kwargs = {
            'username': {'required': False},
            'email': {'required': False},
        }

# ====================== Converting department name to its corresponding id =====================from rest_framework import serializers
class DepartmentNameToIdSerializer(serializers.Serializer):
    """
    Serializer for converting a department name to its corresponding ID.
    """
    department_name = serializers.CharField()

    def validate_department_name(self, value):
        """
        Validate that the department name exists and return its ID(s).
        """
        departments = Department.objects.filter(name=value)
        if not departments.exists():
            raise serializers.ValidationError({"department_name": "Invalid department name."})

        # Handle multiple departments with the same name
        return [department.id for department in departments]


class ProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user profile information.
    """
    user = CustomUserSerializer(partial=True)  # Allow partial updates on user
    department = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), 
        required=False, 
        write_only=True
    )
    department_name = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Profile
        fields = ['user', 'department', 'department_name', 'role']

    def validate(self, data):
        """
        Override the validate method to use DepartmentNameToIdSerializer
        """
        department_name = data.get('department_name')
        if department_name:
            dept_serializer = DepartmentNameToIdSerializer(data={'department_name': department_name})
            if dept_serializer.is_valid():
                # Use the first department ID if multiple IDs are returned
                department_id = dept_serializer.validated_data['department_name'][0]
                data['department'] = department_id
            else:
                raise serializers.ValidationError(dept_serializer.errors)
        return data

    def to_representation(self, instance):
        """
        Customize the representation to include department name.
        """
        representation = super().to_representation(instance)
        representation['department_name'] = instance.department.name if instance.department else None
        return representation

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        department_id = validated_data.pop('department', None)

        # Update the User instance
        if user_data:
            user_instance = instance.user
            user_serializer = CustomUserSerializer(user_instance, data=user_data, partial=True)
            if user_serializer.is_valid():
                user_serializer.save()
            else:
                raise serializers.ValidationError({"user": user_serializer.errors})

        # Update the Department instance (ID assignment)
        if department_id:
            instance.department_id = department_id  # Use the department ID

        # Update other fields
        instance.role = validated_data.get('role', instance.role)
        instance.save()

        return instance





# ===================== Asset Management Serializers ======================

# Serializer for the Category model
class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model.
    """
    class Meta:
        model = Category
        fields = ['id', 'name']

# Serializer for the Tag model
class TagSerializer(serializers.ModelSerializer):
    """
    Serializer for the Tag model.
    """
    class Meta:
        model = Tag
        fields = ['id', 'name', 'barcode_number', 'barcode_image']

# Serializer for the Asset model
class AssetSerializer(serializers.ModelSerializer):
    """
    Serializer for the Asset model.
    """
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Asset
        fields = '__all__'

# ===================== Asset Assignment ======================
class AssetAssignmentSerializer(serializers.ModelSerializer):
    """
    Serializer for the AssetAssignment model.
    """
    class Meta:
        model = AssetAssignment
        fields = ['id', 'asset', 'user', 'assignedTo', 'assignedDepartment', 'returnDate']

# ===================== Asset With Category =================
class AssetWithCategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Asset model with category data.
    """
    category = CategorySerializer()

    class Meta:
        model = Asset
        fields = '__all__'

