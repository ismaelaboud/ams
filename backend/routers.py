<<<<<<< HEAD
# routers.py
from rest_framework import routers
from assets.viewsets import AssetViewSet, CategoryViewSet, TagViewSet, AssetTagViewSet
from assets.viewsets import AssetViewSet, CategoryViewSet, TagViewSet
=======
from django.urls import path
from rest_framework import routers
from assets import views
from assets.viewsets import(
   AssetAssignmentViewSet, AssetViewSet,  AssetCountView
)

>>>>>>> backend
# Initialize the default router
router = routers.DefaultRouter()


# =============== Asset Routers ===========================
# all assets
router.register(r'assets', AssetViewSet, basename='asset')
<<<<<<< HEAD
# Register the AssetTagViewSet with the router
router.register(r'asset-tags', AssetTagViewSet, basename='asset-tag')
=======
#all assets where category is Furnitures
router.register(r'furnitures', AssetViewSet, basename='furnitures')
# count the number of assets filterered by category
router.register(r'assets/count', AssetCountView, basename='asset-count')
router.register(r'asset-assignments', AssetAssignmentViewSet, basename='asset-assignment')


>>>>>>> backend
