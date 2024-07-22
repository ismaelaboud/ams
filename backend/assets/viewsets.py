from django.shortcuts import get_object_or_404  # Import function to retrieve an object or raise a 404 error
from rest_framework import viewsets, generics  # Import viewset and generic views
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny  # Import permission classes
from rest_framework_simplejwt.authentication import JWTAuthentication  # Import JWT authentication class
from django.contrib.auth import get_user_model  # Import function to get the user model
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode  # Import functions for URL-safe base64 encoding/decoding
from django.core.mail import EmailMultiAlternatives  # Import class for sending multi-part emails
from django.template.loader import render_to_string  # Import function to render templates to strings
from django.urls import reverse  # Import function to reverse URL patterns
from django.contrib.auth.tokens import default_token_generator  # Import default token generator for password resets
from rest_framework.response import Response  # Import class for HTTP responses
from rest_framework.views import APIView  # Import base class for API views
from rest_framework import status, views  # Import status codes and base class for views
from rest_framework_simplejwt.tokens import RefreshToken  # Import JWT refresh token class
from assets.models import AssetTag, Category, Profile, Tag, Asset, CustomUser, AssetAssignment  # Import asset-related models
from assets.serializers import (  # Import serializers for asset-related operations
    AssetWithCategorySerializer, CategorySerializer, PasswordResetConfirmSerializer, PasswordResetRequestSerializer, ProfileSerializer,
    ProfileUpdateSerializer, TagSerializer, AssetSerializer, RegisterSerializer, PasswordChangeSerializer,
    AssetAssignmentSerializer, LoginSerializer
)

# ============================== AUTHENTICATION MODULES =============================
class RegisterView(APIView):
    """
    Handles user registration.
    """
    permission_classes = [AllowAny]  # Allow any user to access this view

    def post(self, request):
        """
        Handles POST requests for user registration.
        """
        serializer = RegisterSerializer(data=request.data)  # Initialize serializer with request data
        if serializer.is_valid():
            serializer.save()  # Save the user if the data is valid
            return Response({"message": "Registration successful"}, status=status.HTTP_201_CREATED)
        
        # Combine errors into one message
        errors = serializer.errors
        combined_errors = []
        if 'email' in errors:
            combined_errors.append("User with that email already exists.")  # Append error for email if it exists
        if 'username' in errors:
            combined_errors.append("User with that username already exists.")  # Append error for username if it exists
        if 'password' in errors:
            combined_errors.append(errors['password'][0])  # Append password error if it exists

        return Response({"message": " ".join(combined_errors)}, status=status.HTTP_400_BAD_REQUEST)  # Return combined error messages

class LoginView(APIView):
    """
    Handles user login.
    """
    permission_classes = [AllowAny]  # Allow any user to access this view

    def post(self, request):
        """
        Handles POST requests for user login.
        """
        serializer = LoginSerializer(data=request.data, context={'request': request})  # Initialize serializer with request data and context
        if serializer.is_valid():
            return Response({
                "message": "Login successful",
                "refresh": serializer.validated_data["refresh"],  # Return refresh token
                "access": serializer.validated_data["access"]  # Return access token
            }, status=status.HTTP_200_OK)
        
        # Return a clean error message
        return Response({
            "message": "Invalid login credentials"  # Return error message for invalid credentials
        }, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    """
    Handles user logout.
    """
    authentication_classes = [JWTAuthentication]  # Require JWT authentication for this view
    permission_classes = [IsAuthenticated]  # Allow only authenticated users to access this view

    def post(self, request):
        """
        Handles POST requests for user logout.
        """
        refresh_token = request.data.get('refresh_token')  # Get refresh token from request data
        if not refresh_token:
            return Response({"error": "Refresh token not provided."}, status=status.HTTP_400_BAD_REQUEST)  # Return error if no token provided

        token = RefreshToken(refresh_token)  # Create a RefreshToken instance
        token.blacklist()  # Blacklist the token to invalidate it
        return Response({"message": "User logged out successfully."}, status=status.HTTP_205_RESET_CONTENT)  # Return success message

class PasswordChangeView(APIView):
    """
    Handles password change for authenticated users.
    """
    permission_classes = [IsAuthenticated]  # Allow only authenticated users to access this view

    def post(self, request):
        """
        Handles POST requests for password change.
        """
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})  # Initialize serializer with request data and context
        if serializer.is_valid():
            request.user.set_password(serializer.validated_data['new_password'])  # Set the new password
            request.user.save()  # Save the user with the new password
            return Response({"message": "Password reset successfully."}, status=status.HTTP_200_OK)  # Return success message
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Return validation errors

User = get_user_model()  # Get the user model

class PasswordResetView(viewsets.ViewSet):
    """
    Handles password reset requests.
    """
    serializer_class = PasswordResetRequestSerializer  # Specify serializer class

    def create(self, request):
        """
        Handles POST requests to initiate a password reset.
        """
        serializer = self.serializer_class(data=request.data)  # Initialize serializer with request data
        serializer.is_valid(raise_exception=True)  # Validate data

        email = serializer.validated_data['email']  # Get email from validated data
        
        try:
            user = User.objects.get(email=email)  # Get user by email
        except User.DoesNotExist:
            return Response({"message": "If an account with that email exists, a password reset link has been sent."}, status=status.HTTP_200_OK)  # Return success message if user does not exist

        # Generate password reset token
        reset_token = default_token_generator.make_token(user)  # Create a reset token
        uidb64 = urlsafe_base64_encode(str(user.pk).encode())  # Encode user ID in base64

        # Build reset password URL
        reset_password_url = "{}?uidb64={}&token={}".format(
            request.build_absolute_uri(reverse('reset-password-confirm')),  # Build absolute URI for reset password view
            uidb64,
            reset_token
        )

        # Prepare email content
        context = {
            'username': user.username,
            'reset_password_url': reset_password_url  # Include reset password URL in context
        }

        email_html_message = render_to_string('email/password_reset_email.html', context)  # Render HTML email template
        email_plaintext_message = render_to_string('email/password_reset_email.txt', context)  # Render plain text email template

        msg = EmailMultiAlternatives(
            subject="Password Reset for Your SPH Asset Management Account",  # Set email subject
            body=email_plaintext_message,  # Set plain text email body
            from_email="noreply@gmail.com",  # Set sender email
            to=[user.email]  # Set recipient email
        )
        msg.attach_alternative(email_html_message, "text/html")  # Attach HTML alternative to email
        msg.send()  # Send the email

        return Response({"message": "If an account with that email exists, a password reset link has been sent."}, status=status.HTTP_200_OK)  # Return success message

# =================== Reset password confirmation ============================================
User = get_user_model()  # Get the user model

class PasswordResetConfirmView(views.APIView):
    """
    Handles password reset confirmation.
    """
    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to confirm password reset.
        """
        serializer = PasswordResetConfirmSerializer(data=request.data)  # Initialize serializer with request data
        if serializer.is_valid():
            uidb64 = serializer.validated_data.get('uidb64')  # Get UID from validated data
            token = serializer.validated_data.get('token')  # Get reset token from validated data
            new_password = serializer.validated_data.get('new_password')  # Get new password from validated data

            try:
                uid = urlsafe_base64_decode(uidb64).decode()  # Decode UID from base64
                user = User.objects.get(pk=uid)  # Get user by UID
            except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
                return Response({'error': 'Invalid token or user'}, status=status.HTTP_400_BAD_REQUEST)  # Return error if token or user is invalid
            
            if default_token_generator.check_token(user, token):  # Check if token is valid
                user.set_password(new_password)  # Set the new password
                user.save()  # Save the user with the new password
                return Response({'message': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)  # Return success message
            else:
                return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)  # Return error if token is invalid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Return validation errors

# ================= Retrieving and entering data to and from the Asset model ===========================

class AssetViewSet(viewsets.ModelViewSet):
    """
    Handles CRUD operations for Asset model.
    """
    queryset = Asset.objects.all()  # Set the queryset for all assets
    serializer_class = AssetSerializer  # Specify serializer class

    def get_permissions(self):
        """
        Sets permissions based on the request method.
        """
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAdminUser]  # Allow only admin users for POST, PUT, PATCH, DELETE methods
        else:
            self.permission_classes = [IsAuthenticated]  # Allow authenticated users for other methods
        return super().get_permissions()  # Return the permissions

class AssetCategoryFilterViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Filters assets by category and provides read-only access.
    """
    serializer_class = AssetWithCategorySerializer  # Specify serializer class
    permission_classes = [IsAuthenticated]  # Allow only authenticated users to access this view

    def get_queryset(self):
        """
        Returns queryset filtered by category name if provided.
        """
        category_name = self.request.query_params.get('category_name', None)  # Get category name from query parameters
        if category_name:
            return Asset.objects.filter(category__name=category_name)  # Filter assets by category name
        return Asset.objects.all()  # Return all assets if no category name is provided

    def list(self, request, *args, **kwargs):
        """
        Lists filtered assets with count.
        """
        queryset = self.get_queryset()  # Get the filtered queryset
        serializer = self.get_serializer(queryset, many=True)  # Serialize the queryset
        response_data = {
            'count': queryset.count(),  # Include the count of assets
            'results': serializer.data  # Include serialized data of assets
        }
        return Response(response_data, status=status.HTTP_200_OK)  # Return the response with asset data

# ============================== Manipulating a single asset in Asset model ===================================

class AssetDetailView(APIView):
    """
    Provides detailed operations for a single asset.
    """
    def get(self, request, id):
        """
        Retrieves a single asset by ID.
        """
        asset = get_object_or_404(Asset.objects.select_related('category', 'assignedDepartment'), id=id)  # Retrieve asset by ID or raise 404
        serializer = AssetWithCategorySerializer(asset)  # Serialize the asset
        return Response(serializer.data, status=status.HTTP_200_OK)  # Return the response with asset data

    def put(self, request, id):
        """
        Updates a single asset by ID.
        """
        asset = get_object_or_404(Asset, id=id)  # Retrieve asset by ID or raise 404
        serializer = AssetSerializer(asset, data=request.data)  # Initialize serializer with request data
        if serializer.is_valid():
            serializer.save()  # Save the updated asset
            return Response(serializer.data, status=status.HTTP_200_OK)  # Return the updated asset data
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Return validation errors

    def patch(self, request, id):
        """
        Partially updates a single asset by ID.
        """
        asset = get_object_or_404(Asset, id=id)  # Retrieve asset by ID or raise 404
        serializer = AssetSerializer(asset, data=request.data, partial=True)  # Initialize serializer with partial update data
        if serializer.is_valid():
            serializer.save()  # Save the partially updated asset
            return Response({"msg": "Updated successfully"}, status=status.HTTP_200_OK)  # Return success message
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Return validation errors

    def delete(self, request, id):
        """
        Deletes a single asset by ID.
        """
        asset = get_object_or_404(Asset, id=id)  # Retrieve asset by ID or raise 404
        asset.delete()  # Delete the asset
        return Response({"message": "Asset deleted successfully"}, status=status.HTTP_204_NO_CONTENT)  # Return success message
