from django.contrib.auth import authenticate, get_user_model  # Import authentication and user model utilities
from rest_framework import serializers  # Import serializers from Django REST Framework
from rest_framework_simplejwt.tokens import RefreshToken  # Import RefreshToken for JWT
from django.contrib.auth.password_validation import validate_password  # Import password validation
from assets.models import CustomUser, Category, Tag, Asset, Department, Profile, AssetAssignment  # Import models

# ====================== Custom User Serializer =======================
class UserSerializer(serializers.ModelSerializer):  # Define UserSerializer for CustomUser model
    """
    Serializer for the CustomUser model to handle user data.
    """
    class Meta:
        model = CustomUser  # Specify model
        fields = ['id', 'username', 'email', 'firstName', 'lastName', 'date_joined']  # Define fields to serialize

# ========================== USER MANAGEMENT SERIALIZERS MODULES =============================
# Serializer for user registration
class RegisterSerializer(serializers.ModelSerializer):  # Define RegisterSerializer for user registration
    """
    Serializer for registering a new user.
    """
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])  # Password field with validation
    password2 = serializers.CharField(write_only=True, required=True)  # Confirm password field

    class Meta:
        model = CustomUser  # Specify model
        fields = ['firstName', 'lastName', 'email', 'username', 'password', 'password2']  # Define fields to serialize

    def validate(self, attrs):  # Validate registration data
        """
        Validate that password and password2 match and check for unique email and username.
        """
        if attrs['password'] != attrs['password2']:  # Check if passwords match
            raise serializers.ValidationError({"password": "Password fields didn't match."})  # Raise error if not

        if CustomUser.objects.filter(email=attrs['email']).exists():  # Check if email is unique
            raise serializers.ValidationError({"email": "User with that email already exists."})  # Raise error if not

        if CustomUser.objects.filter(username=attrs['username']).exists():  # Check if username is unique
            raise serializers.ValidationError({"username": "User with that username already exists."})  # Raise error if not

        return attrs  # Return validated data

    def create(self, validated_data):  # Create a new user
        """
        Create a new user with the validated data.
        """
        validated_data.pop('password2')  # Remove password2 from validated data
        user = CustomUser.objects.create(  # Create user instance
            firstName=validated_data['firstName'],
            lastName=validated_data['lastName'],
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])  # Set the user's password
        user.save()  # Save the user instance
        return user  # Return created user

    def to_representation(self, instance):  # Customize the representation of the user data
        """
        Customize the representation of the user data, excluding the password fields.
        """
        response = super().to_representation(instance)  # Get the default representation
        response.pop('password', None)  # Remove password from response
        response.pop('password2', None)  # Remove password2 from response
        return response  # Return modified representation

# Serializer for user login
class LoginSerializer(serializers.Serializer):  # Define LoginSerializer for user login
    """
    Serializer for user login.
    """
    usernameOrEmail = serializers.CharField()  # Field for username or email
    password = serializers.CharField(write_only=True)  # Field for password
    access = serializers.CharField(read_only=True)  # Field for access token
    refresh = serializers.CharField(read_only=True)  # Field for refresh token

    def validate(self, attrs):  # Validate login credentials
        """
        Validate login credentials and generate JWT tokens.
        """
        usernameOrEmail = attrs.get('usernameOrEmail')  # Get username or email
        password = attrs.get('password')  # Get password

        if not usernameOrEmail or not password:  # Check if both fields are provided
            raise serializers.ValidationError("Username/Email and password are required")  # Raise error if not

        # Try to authenticate with the username_or_email as username first
        user = authenticate(username=usernameOrEmail, password=password)  # Authenticate with username

        if user is None:  # If authentication fails, try with email
            try:
                user_obj = CustomUser.objects.get(email=usernameOrEmail)  # Get user by email
                user = authenticate(username=user_obj.username, password=password)  # Authenticate with username from user object
            except CustomUser.DoesNotExist:  # If user does not exist
                raise serializers.ValidationError("Invalid login credentials")  # Raise error for invalid credentials

        if user is None:  # If user is still None
            raise serializers.ValidationError("Invalid login credentials")  # Raise error for invalid credentials

        refresh = RefreshToken.for_user(user)  # Generate refresh token for the user
        attrs['refresh'] = str(refresh)  # Add refresh token to attributes
        attrs['access'] = str(refresh.access_token)  # Add access token to attributes
        attrs['user'] = user  # Add user to attributes

        return attrs  # Return validated data

# ===================== User Changing password ===============================
class PasswordChangeSerializer(serializers.Serializer):  # Define PasswordChangeSerializer for changing passwords
    """
    Serializer for changing user password.
    """
    oldPassword = serializers.CharField(write_only=True)  # Field for old password
    newPassword = serializers.CharField(write_only=True)  # Field for new password
    newPasswordConfirm = serializers.CharField(write_only=True)  # Field for new password confirmation

    def validate(self, data):  # Validate the new passwords
        """
        Validate that new passwords match.
        """
        if data['newPassword'] != data['newPasswordConfirm']:  # Check if new passwords match
            raise serializers.ValidationError("New passwords do not match")  # Raise error if not

        return data  # Return validated data

    def validate_oldPassword(self, value):  # Validate the old password
        """
        Validate that the old password is correct.
        """
        user = self.context['request'].user  # Get the user from request context
        if not user.check_password(value):  # Check if old password is correct
            raise serializers.ValidationError("Old password is incorrect")  # Raise error if not

        return value  # Return validated old password

# ================= Reseting user password by sending reset token to email =================
class PasswordResetRequestSerializer(serializers.Serializer):  # Define PasswordResetRequestSerializer for password reset requests
    """
    Serializer for requesting a password reset via email.
    """
    email = serializers.EmailField()  # Field for email address

    def validate_email(self, value):  # Validate the email address
        """
        Validate that the email exists in the system.
        """
        if not CustomUser.objects.filter(email=value).exists():  # Check if email exists
            raise serializers.ValidationError("There is no user registered with this email address.")  # Raise error if not

        return value  # Return validated email address

# ================ Confirm password reset =============================
class PasswordResetConfirmSerializer(serializers.Serializer):  # Define PasswordResetConfirmSerializer for confirming password reset
    """
    Serializer for confirming password reset with a token.
    """
    uidb64 = serializers.CharField()  # Field for UID
    token = serializers.CharField()  # Field for token
    new_password = serializers.CharField(max_length=128, write_only=True)  # Field for new password
    confirm_new_password = serializers.CharField(max_length=128, write_only=True)  # Field for new password confirmation

    def validate(self, attrs):  # Validate the reset data
        """
        Validate that new passwords match.
        """
        new_password = attrs.get('new_password')  # Get new password
        confirm_new_password = attrs.get('confirm_new_password')  # Get confirm new password

        if new_password != confirm_new_password:  # Check if new passwords match
            raise serializers.ValidationError("Passwords do not match.")  # Raise error if not

        return attrs  # Return validated data

# ==================== User Profile ======================
class DepartmentSerializer(serializers.ModelSerializer):  # Define DepartmentSerializer for Department model
    """
    Serializer for the Department model.
    """
    class Meta:
        model = Department  # Specify model
        fields = ['name']  # Define fields to serialize

class ProfileSerializer(serializers.ModelSerializer):  # Define ProfileSerializer for Profile model
    """
    Serializer for the Profile model.
    """
    department = DepartmentSerializer(read_only=True)  # Use DepartmentSerializer for department field
    user = UserSerializer(read_only=True)  # Use UserSerializer for user field

    class Meta:
        model = Profile  # Specify model
        fields = ['id', 'user', 'department', 'role']  # Define fields to serialize
        read_only_fields = ['user', 'department', 'role']  # Define read-only fields

class CustomUserSerializer(serializers.ModelSerializer):  # Define CustomUserSerializer with optional fields
    """
    Serializer for the CustomUser model with optional fields.
    """
    class Meta:
        model = CustomUser  # Specify model
        fields = ['id', 'username', 'email', 'firstName', 'lastName', 'date_joined']  #
