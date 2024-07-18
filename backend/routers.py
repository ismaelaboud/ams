from django.urls import path
from rest_framework import routers
from assets import views
from assets.viewsets import(
   AssetAssignmentViewSet, AssetViewSet,  AssetCountView
)

# Initialize the default router
router = routers.DefaultRouter()


# =============== Asset Routers ===========================
# all assets
router.register(r'assets', AssetViewSet, basename='asset')
#all assets where category is Furnitures
router.register(r'furnitures', AssetViewSet, basename='furnitures')
# count the number of assets filterered by category
router.register(r'assets/count', AssetCountView, basename='asset-count')
router.register(r'asset-assignments', AssetAssignmentViewSet, basename='asset-assignment')


