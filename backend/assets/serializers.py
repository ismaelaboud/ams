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
    departmentName = serializers.CharField()

    def validate_departmentName(self, value):
        """
        Validate that the department name exists and return its ID(s).
        """
        departments = Department.objects.filter(name=value)
        if not departments.exists():
            raise serializers.ValidationError("Invalid department name.")
        
        # Return the ID of the first department found with the name
        return departments.first().id


# ====================== Converting category name to its corresponding id =====================
class CategoryNameToIdSerializer(serializers.Serializer):
    """
    Serializer for converting a category name to its corresponding ID.
    """
    category = serializers.CharField()

    def validate_category(self, value):
        """
        Validate that the category name exists and return its ID.
        """
        categories = Category.objects.filter(name=value)
        if not categories.exists():
            raise serializers.ValidationError("Invalid category name.")
        
        # Return the ID of the first category found with the name
        return categories.first().id

class ProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user profile information.
    """
    user = CustomUserSerializer(partial=True)
    department = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), 
        required=False, 
        write_only=True
    )
    departmentName = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Profile
        fields = ['user', 'department', 'departmentName', 'role']

    def validate(self, data):
        """
        Override the validate method to use DepartmentNameToIdSerializer.
        """
        departmentName = data.get('departmentName')
        if departmentName:
            dept_serializer = DepartmentNameToIdSerializer(data={'departmentName': departmentName})
            if dept_serializer.is_valid():
                # Use the first department ID returned
                department_id = dept_serializer.validated_data['departmentName']
                data['department'] = department_id
            else:
                raise serializers.ValidationError(dept_serializer.errors)
        return data

    def to_representation(self, instance):
        """
        Customize the representation to include department name.
        """
        representation = super().to_representation(instance)
        representation['departmentName'] = instance.department.name if instance.department else None
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

        # Update the Department (ID assignment)
        if department_id is not None:
            instance.department_id = department_id

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
    category = serializers.CharField(write_only=True)  # Accept as string
    categoryId = serializers.IntegerField(read_only=True, source='category.id')
    categoryName = serializers.CharField(read_only=True, source='category.name')
    departmentName = serializers.CharField(write_only=True, required=False)
    assignedDepartment = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all(), write_only=True, required=False)

    class Meta:
        model = Asset
        fields = '__all__'

    def validate(self, data):
        # Validate and convert category
        category_value = data.pop('category', None)
        if category_value:
            try:
                category = Category.objects.get(id=int(category_value))
            except (ValueError, Category.DoesNotExist):
                category = Category.objects.filter(name=category_value).first()
                if not category:
                    raise serializers.ValidationError({'category': 'Category not found.'})
            data['category'] = category

        # Convert department name to Department instance if provided
        department_name = data.pop('departmentName', None)
        if department_name:
            department = Department.objects.filter(name=department_name).first()
            if not department:
                raise serializers.ValidationError({'departmentName': 'Department not found.'})
            data['assignedDepartment'] = department  # Assign the Department instance

        return data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['categoryName'] = instance.category.name if instance.category else None
        representation['departmentName'] = instance.assignedDepartment.name if instance.assignedDepartment else None
        return representation

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

