from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator 
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, views
from rest_framework_simplejwt.tokens import RefreshToken
from assets.models import AssetTag, Category, Department, Profile, Tag, Asset, CustomUser, AssetAssignment
from assets.serializers import (
    AssetWithCategorySerializer, CategorySerializer, DepartmentSerializer, PasswordResetConfirmSerializer, PasswordResetRequestSerializer, ProfileSerializer,
    ProfileUpdateSerializer, TagSerializer, AssetSerializer, RegisterSerializer, PasswordChangeSerializer,
    AssetAssignmentSerializer, LoginSerializer
)

# ============================== AUTHENTICATION MODULES =============================
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Registration successful"}, status=status.HTTP_201_CREATED)
        
        # Combine errors into one message
        errors = serializer.errors
        combined_errors = []
        if 'email' in errors:
            combined_errors.append("User with that email already exists.")
        if 'username' in errors:
            combined_errors.append("User with that username already exists.")
        if 'password' in errors:
            combined_errors.append(errors['password'][0])

        return Response({"message": " ".join(combined_errors)}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            return Response({
                "message": "Login successful",
                "refresh": serializer.validated_data["refresh"],
                "access": serializer.validated_data["access"]
            }, status=status.HTTP_200_OK)
        
        # Return a clean error message
        return Response({
            "message": "Invalid login credentials"
        }, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return Response({"error": "Refresh token not provided."}, status=status.HTTP_400_BAD_REQUEST)

        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message": "User logged out successfully."}, status=status.HTTP_205_RESET_CONTENT)

class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            request.user.set_password(serializer.validated_data['newPassword'])
            request.user.save()
            return Response({"message": "Password reset successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

User = get_user_model()

class PasswordResetView(views.APIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"message": "If an account with that email exists, a password reset link has been sent."}, status=status.HTTP_200_OK)

        reset_token = default_token_generator.make_token(user)
        uidb64 = urlsafe_base64_encode(str(user.pk).encode())

        # Point the reset link to the frontend URL
        frontend_reset_password_url = "http://127.0.0.1:3000/reset?uidb64={}&token={}".format(
            uidb64,
            reset_token
        )

        context = {
            'username': user.username,
            'reset_password_url': frontend_reset_password_url
        }

        email_html_message = render_to_string('email/password_reset_email.html', context)
        email_plaintext_message = render_to_string('email/password_reset_email.txt', context)

        msg = EmailMultiAlternatives(
            subject="Password Reset for Your SPH Asset Management Account",
            body=email_plaintext_message,
            from_email="noreply@gmail.com",
            to=[user.email]
        )
        msg.attach_alternative(email_html_message, "text/html")
        msg.send()

        return Response({"message": "If an account with that email exists, a password reset link has been sent."}, status=status.HTTP_200_OK)

class PasswordResetConfirmView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            uidb64 = serializer.validated_data.get('uidb64')
            token = serializer.validated_data.get('token')
            new_password = serializer.validated_data.get('new_password')

            try:
                uid = urlsafe_base64_decode(uidb64).decode()
                user = User.objects.get(pk=uid)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                return Response({'error': 'Invalid token or user'}, status=status.HTTP_400_BAD_REQUEST)

            if default_token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
                return Response({'message': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# ================= Retrieving and entering data to and from the Asset model ===========================

class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

class AssetCategoryFilterViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AssetWithCategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        category_name = self.request.query_params.get('category_name', None)
        if category_name:
            return Asset.objects.filter(category__name=category_name)
        return Asset.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response_data = {
            'count': queryset.count(),
            'results': serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)

# ============================== Manipulating a single asset in Asset model ===================================

class AssetDetailView(APIView):
    def get(self, request, id):
        asset = get_object_or_404(Asset.objects.select_related('category', 'assignedDepartment'), id=id)
        serializer = AssetWithCategorySerializer(asset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        asset = get_object_or_404(Asset, id=id)
        serializer = AssetSerializer(asset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id):
        asset = get_object_or_404(Asset, id=id)
        serializer = AssetSerializer(asset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        asset = get_object_or_404(Asset, id=id)
        asset.delete()
        return Response({"msg": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

# ============================ CRUD AssetAssignments ===========================

class AssetAssignmentViewSet(viewsets.ModelViewSet):
    queryset = AssetAssignment.objects.all()
    serializer_class = AssetAssignmentSerializer

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

# ============================ Profiles with departments ========================

class UserProfileViewSet(generics.RetrieveUpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        """
        Return the profile of the currently authenticated user.
        If the profile does not exist, create one.
        """
        user = self.request.user
        try:
            return user.profile
        except Profile.DoesNotExist:
            # Optionally, create the profile if it doesn't exist
            profile = Profile.objects.create(user=user)
            return profile

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ProfileUpdateSerializer
        return ProfileSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)



# ============================ Categories, Tags ==============================

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

class AssetTagViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing tag instances.
    """
    queryset = Tag.objects.all()  # Defines the set of Tag objects this viewset will operate on
    serializer_class = TagSerializer  # Specifies the serializer to use for the Tag model

    def get_permissions(self):
        """
        Returns the list of permission classes that are allowed for this viewset.
        - Admin users are required for POST, PUT, PATCH, DELETE methods.
        - Authenticated users are allowed for GET method.
        """
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAdminUser]  # Only admin users can create, update, or delete tags
        else:
            self.permission_classes = [IsAuthenticated]  # Authenticated users can view tags
        
        return super().get_permissions()

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def list(self, request, *args, **kwargs):
        """
        Override the list method to provide custom validation and error handling.
        """
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        """
        Override the retrieve method to provide custom validation and error handling.
        """
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Category.DoesNotExist:
            return Response({'detail': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class DepartmentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing departments.
    """
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def list(self, request, *args, **kwargs):
        """
        Override the list method to provide custom validation and error handling.
        """
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        """
        Override the retrieve method to provide custom validation and error handling.
        """
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Department.DoesNotExist:
            return Response({'detail': 'Department not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)