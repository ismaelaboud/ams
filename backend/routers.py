from django.urls import path, include
from rest_framework import routers
from assets.viewsets import AssetViewSet, CategoryViewSet, TagViewSet

# Initialize the default router
router = routers.DefaultRouter()

# Register the CategoryViewSet with the router
router.register(r'categories', CategoryViewSet, basename='category')

# Register the TagViewSet with the router
router.register(r'tags', TagViewSet, basename='tag')

# Register the AssetViewSet with the router
router.register(r'assets', AssetViewSet, basename='asset')

# Define the URL patterns
urlpatterns = [
    path('api/', include(router.urls)),  # Include all registered router URLs under the /api/ path
]
