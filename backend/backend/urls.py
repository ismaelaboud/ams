from django.contrib import admin
from django.urls import path, include
from assets import views
from routers import router  # Import router from the root directory
from assets.tests import Test
from assets.viewsets import (
    AssetDetailView, PasswordChangeView, PasswordResetConfirmView, PasswordResetView, 
    RegisterView, LoginView, LogoutView,
    AssetAssignmentViewSet, UserProfileViewSet
)

# Define your urlpatterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # Ensure router is correctly defined
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    path('api/auth/login/', LoginView.as_view(), name='login'),
    path('api/password_reset/', PasswordResetView.as_view(), name='password-reset-request'),
    path('api/reset-password-confirm/', PasswordResetConfirmView.as_view(), name='reset-password-confirm'),
    path('api/auth/logout/', LogoutView.as_view(), name='logout'),
    path('api/profile/', UserProfileViewSet.as_view(), name='user-profile'),
    path('api/auth/change_password/', PasswordChangeView.as_view(), name='change_password'),
    path('api/assets/detail/<int:id>/', AssetDetailView.as_view(), name='asset_detail'),
]
