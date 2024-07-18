# backend/urls.py

from webbrowser import get
from django.contrib import admin
from django.urls import path, include
from assets import views
from routers import router  # Import router from the root directory
from assets.viewsets import(
 AssetDetailView, RegisterView, LoginView, LogoutView, PasswordResetView, AssetAssignmentViewSet
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # Include the API routes from the router
    path('api/auth/register/', RegisterView.as_view(), name='register'),  # Add user registration route
    path('api/auth/login/', LoginView.as_view(), name='login'),  # Add user login route
    path('api/auth/logout/', LogoutView.as_view(), name='logout'),
    path('api/auth/password_reset/', PasswordResetView.as_view(), name='password_reset'),
     
    # ================= Assets urls =================
     path('api/assets/detail/<int:id>/', AssetDetailView.as_view(), name='asset_detail'),
]
