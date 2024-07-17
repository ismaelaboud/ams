from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate
from assets.models import Category, Tag, Asset, CustomUser
from assets.serializers import CategorySerializer, TagSerializer, AssetSerializer, RegisterSerializer, LoginSerializer, PasswordResetSerializer

# ================== User registration logic ====================
class RegisterView(APIView):
    """
    API view to register a new user.
    """
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# =============== User login logic =================
class LoginView(APIView):
    """
    API view to login a user and provide JWT tokens.
    """
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ================== User logout logic ==================
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

# ==================== User Password Reset Logic =============================
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


# =================== Pulling all assets categories logic ==================
class CategoryViewSet(viewsets.ModelViewSet):
    """
    Viewset for handling CRUD operations on Category objects.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]  # Requires authentication for all actions


# ====================== Pulling all tags from the database =================
class TagViewSet(viewsets.ModelViewSet):
    """
    Viewset for handling CRUD operations on Tag objects.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]  # Requires authentication for all actions

# ==================== Pulling all assets from the database =====================
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
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            return [IsAdminUser()]  # Requires admin permission for write operations
        else:
            return [IsAuthenticated()]  # Requires authentication for other actions

