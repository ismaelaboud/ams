from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import authenticate
from assets.models import Category, Profile, Tag, Asset, CustomUser, AssetAssignment
from assets.serializers import(
    CategorySerializer, TagSerializer, AssetSerializer, RegisterSerializer,
    PasswordResetSerializer, AssetAssignmentSerializer, LoginSerializer
)

# ============================== AUTHENTICATION MODULES =============================
class RegisterView(APIView):
    """
    API view to register a new user.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Registration successful"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    """
    API view to login a user and provide JWT tokens.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Login successful",
                "refresh": serializer.validated_data["refresh"],
                "access": serializer.validated_data["access"]
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """
    API view to logout an authenticated user.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            if refresh_token is None:
                return Response({"error": "Refresh token not provided."}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "User logged out successfully."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetView(APIView):
    """
    API view to reset a user's password by providing the old password.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']

            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                return Response({"message": "Password reset successfully."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Old password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ================= Retriving and entering data to and from the Asset model ===========================
class AssetViewSet(viewsets.ModelViewSet):
    """
    Viewset for handling CRUD operations on Asset objects.
    """
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer

    def get_permissions(self):
        """
        Custom method to determine permissions based on the request method.
        """
        if self.request.method in ['POST']:
            self.permission_classes = [IsAdminUser]  # Requires admin permission for write operations
        else:
            self.permission_classes = [IsAuthenticated]  # Requires authentication for other actions

        return super().get_permissions()

class AssetCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Viewset for filtering assets where category equals to 'Furnitures'.
    """
    serializer_class = AssetSerializer

    def get_queryset(self):
        return Asset.objects.filter(category='Furnitures')
    
class AssetCountView(viewsets.ViewSet):
    def list(self, request, *args, **kwargs):
        count = Asset.objects.filter(category__name='Furnitures').count()
        return Response({'count': count})
    

# ============================== Manipulating a single asset in Asset model ===================================
class AssetDetailView(APIView):
    def get(self, request, id):
        try:
            asset = Asset.objects.select_related('category', 'assignedDepartment').get(id=id)
            data = {
                'id': asset.id,
                'category': {
                    'id': asset.category.id,
                    'name': asset.category.name
                },
                'name': asset.name,
                'assetType': asset.assetType,
                'description': asset.description,
                'serialNumber': asset.serialNumber,
                'dateRecorded': asset.dateRecorded.isoformat(),
                'status': asset.status,
                'assignedDepartment': asset.assignedDepartment.id
            }
            return Response(data, status=status.HTTP_200_OK)
        except Asset.DoesNotExist:
            return Response({"msg": "Not Found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id):
        try:
            obj = Asset.objects.get(id=id)
        except Asset.DoesNotExist:
            msg = {"msg": "Not Found"}
            return Response(msg, status=status.HTTP_404_NOT_FOUND)
        serializer = AssetSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_205_RESET_CONTENTS)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
    def patch(self, request, id):
        try:
            asset = Asset.objects.get(id=id)
        except Asset.DoesNotExist:
            msg = {"msg": "Asset not found"}
            return Response(msg, status=status.HTTP_404_NOT_FOUND)
        
        serializer = AssetSerializer(asset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            msg = {"msg": "Updated successfully "}
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            obj = Asset.objects.get(id=id)
            obj.delete()
            return Response({"msg": "Deleted Successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Asset.DoesNotExist:
            msg = {"msg": "Not Found"}
            return Response(msg, status=status.HTTP_404_NOT_FOUND)

# ===========================Assigning Asset to a partucular User ==============================           

class AssetAssignmentViewSet(viewsets.ModelViewSet):
    queryset = AssetAssignment.objects.all()
    serializer_class = AssetAssignmentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        asset = serializer.validated_data['asset']
        asset.status = 'Booked'
        asset.save()
        serializer.save()

    def create(self, request, *args, **kwargs):
        if request.user.is_anonymous or not hasattr(request.user, 'profile'):
            raise PermissionDenied("Only authenticated admins can assign assets.")
        if not request.user.profile.role == Profile.ADMIN_ROLE:
            return Response({"detail": "Only admins can assign assets."}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=['get'], url_path='user-assets/(?P<user_id>[^/.]+)')
    def get_assets_by_user(self, request, user_id=None):
        assignments = AssetAssignment.objects.filter(user_id=user_id)
        assets = [assignment.asset for assignment in assignments]
        serializer = AssetSerializer(assets, many=True)
        return Response(serializer.data)

