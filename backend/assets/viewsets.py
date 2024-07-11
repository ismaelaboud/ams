# viewsets.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import User, Asset, Category, Tag, Role, Department
from .serializers import UserSerializer, AssetSerializer, CategorySerializer, TagSerializer, RoleSerializer, DepartmentSerializer


