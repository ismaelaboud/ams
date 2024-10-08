from django.urls import path
from rest_framework import routers
from assets import views
from assets.viewsets import(
   AssetAssignmentViewSet, AssetCategoryFilterViewSet, AssetTagViewSet, AssetViewSet, CategoryViewSet, DepartmentViewSet,
       UserProfileViewSet
)

# Initialize the default router
router = routers.DefaultRouter()


# =============== Asset Routers ===========================
# all assets
router.register(r'assets', AssetViewSet, basename='asset')
#all assets where category is Furnitures
router.register(r'assets-by-category', AssetCategoryFilterViewSet, basename='asset-category-filter')
# Register the AssetTagViewSet with the router
router.register(r'asset-tags', AssetTagViewSet, basename='asset-tag')
router.register(r'asset-assignments', AssetAssignmentViewSet, basename='asset-assignment')


router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'categories', CategoryViewSet, basename='category')
