from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from assets.models import Category, Tag, Asset, CustomUser
from assets.serializers import CategorySerializer, TagSerializer, AssetSerializer, RegisterSerializer, LoginSerializer
from assets.models import AssetTag
from assets.serializers import AssetTagSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    Viewset for handling CRUD operations on Category objects.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]  # Requires authentication for all actions

class TagViewSet(viewsets.ModelViewSet):
    """
    Viewset for handling CRUD operations on Tag objects.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]  # Requires authentication for all actions

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
            self.permission_classes = [IsAdminUser]  # Requires admin permission for write operations
        else:
            self.permission_classes = [IsAuthenticated]  # Requires authentication for other actions

        return super(AssetViewSet, self).get_permissions()

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

class LoginView(APIView):
    """
    API view to login a user and provide JWT tokens.
    """
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class AssetTagViewSet(viewsets.ModelViewSet):
    queryset = AssetTag.objects.all()
    serializer_class = AssetTagSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
        Custom method to determine permissions based on the request method.
        """
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            self.permission_classes = [IsAdminUser]  # Requires admin permission for write operations
        else:
            self.permission_classes = [IsAuthenticated]  # Requires authentication for other actions

        return super(AssetTagViewSet, self).get_permissions()