from django.urls import path
from rest_framework import routers
from assets import views
from assets.viewsets import(
   AssetAssignmentViewSet, AssetCategoryFilterViewSet, AssetTagViewSet, AssetViewSet,
       UserProfileViewSet
)

# Initialize the default router
router = routers.DefaultRouter()

# =============== User Profile ===========================
router.register(r'user-profiles', UserProfileViewSet, basename='user-profile')

# =============== Asset Routers ===========================
# all assets
router.register(r'assets', AssetViewSet, basename='asset')
#all assets where category is Furnitures
router.register(r'assets-by-category', AssetCategoryFilterViewSet, basename='asset-category-filter')
# Register the AssetTagViewSet with the router
router.register(r'asset-tags', AssetTagViewSet, basename='asset-tag')
router.register(r'asset-assignments', AssetAssignmentViewSet, basename='asset-assignment')
