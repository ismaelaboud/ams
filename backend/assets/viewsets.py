# viewsets.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import CustomUser, Asset, Category, Tag, Department, AssetAssignment
from .serializers import UserSerializer, AssetSerializer, CategorySerializer, TagSerializer, RoleSerializer, DepartmentSerializer


