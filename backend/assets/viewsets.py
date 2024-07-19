from django.shortcuts import get_object_or_404
from rest_framework import viewsets,  generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from assets.models import AssetTag, Category, Profile, Tag, Asset, CustomUser, AssetAssignment
from assets.serializers import(
    AssetWithCategorySerializer, CategorySerializer, ProfileSerializer, ProfileUpdateSerializer, TagSerializer, AssetSerializer, RegisterSerializer,
    PasswordResetSerializer, AssetAssignmentSerializer, LoginSerializer
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

class PasswordResetView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            request.user.set_password(serializer.validated_data['new_password'])
            request.user.save()
            return Response({"message": "Password reset successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ================= Retriving and entering data to and from the Asset model ===========================
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
        asset = get_object_or_404(Asset.objects.select_related('category', 'assigned_department'), id=id)
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
        # Assuming you want to update the profile of the currently logged-in user
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
