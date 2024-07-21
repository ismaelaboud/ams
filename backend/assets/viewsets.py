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
from assets.models import AssetTag, Category, Profile, Tag, Asset, CustomUser, AssetAssignment
from assets.serializers import (
    AssetWithCategorySerializer, CategorySerializer, PasswordResetConfirmSerializer, PasswordResetRequestSerializer, ProfileSerializer,
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
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
            request.user.set_password(serializer.validated_data['new_password'])
            request.user.save()
            return Response({"message": "Password reset successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

User = get_user_model()

class PasswordResetView(viewsets.ViewSet):
    serializer_class = PasswordResetRequestSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"message": "If an account with that email exists, a password reset link has been sent."}, status=status.HTTP_200_OK)

        # Generate password reset token
        reset_token = default_token_generator.make_token(user)
        uidb64 = urlsafe_base64_encode(str(user.pk).encode())

        # Build reset password URL
        reset_password_url = "{}?uidb64={}&token={}".format(
            request.build_absolute_uri(reverse('reset-password-confirm')),
            uidb64,
            reset_token
        )

        # Prepare email content
        context = {
            'username': user.username,
            'reset_password_url': reset_password_url
        }

        email_html_message = render_to_string('email/password_reset_email.html', context)
        email_plaintext_message = render_to_string('email/password_reset_email.txt', context)

        msg = EmailMultiAlternatives(
            subject="Password Reset for Your Website Title",
            body=email_plaintext_message,
            from_email="your-email@example.com",
            to=[user.email]
        )
        msg.attach_alternative(email_html_message, "text/html")
        msg.send()

        return Response({"message": "If an account with that email exists, a password reset link has been sent."}, status=status.HTTP_200_OK)

# =================== Reset password confirmation ============================================
User = get_user_model()

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
            except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
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

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

class ProfileUpdateView(generics.UpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

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
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()
