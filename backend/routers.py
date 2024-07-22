from django.urls import path
from rest_framework import routers
from assets import views
from assets.viewsets import(
   AssetAssignmentViewSet, AssetCategoryFilterViewSet, AssetTagViewSet, AssetViewSet,
       UserProfileViewSet
)

# Initialize the default router
router = routers.DefaultRouter()

"""
The following section registers the viewsets with the router. 
Each viewset is associated with a URL prefix and a basename.
"""

# =============== User Profile ===========================
# Register the UserProfileViewSet with the router.
# The URL pattern will be 'user_profiles/' and the basename for this route is 'user-profile'.
router.register(r'user_profiles', UserProfileViewSet, basename='user-profile')

# =============== Asset Routers ===========================
# Register the AssetViewSet with the router.
# The URL pattern will be 'assets/' and the basename for this route is 'asset'.
router.register(r'assets', AssetViewSet, basename='asset')

# Register the AssetCategoryFilterViewSet with the router.
# The URL pattern will be 'assets-by-category/' and the basename for this route is 'asset-category-filter'.
# This viewset filters assets based on their category, such as 'Furnitures'.
router.register(r'assets-by-category', AssetCategoryFilterViewSet, basename='asset-category-filter')

# Register the AssetTagViewSet with the router.
# The URL pattern will be 'asset-tags/' and the basename for this route is 'asset-tag'.
router.register(r'asset-tags', AssetTagViewSet, basename='asset-tag')

# Register the AssetAssignmentViewSet with the router.
# The URL pattern will be 'asset-assignments/' and the basename for this route is 'asset-assignment'.
router.register(r'asset-assignments', AssetAssignmentViewSet, basename='asset-assignment')
