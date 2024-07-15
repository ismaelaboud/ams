# viewsets.py
from rest_framework import viewsets
from .models import Category, Tag, Asset
from .serializers import CategorySerializer, TagSerializer, AssetSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser

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
