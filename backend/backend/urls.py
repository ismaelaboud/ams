from django.contrib import admin
from django.urls import path, include
from assets import views
from routers import router  # Import router from the root directory
from assets.tests import Test
from assets.viewsets import (
    AssetDetailView, PasswordChangeView, PasswordResetConfirmView, PasswordResetView, ProfileUpdateView,
    RegisterView, LoginView, LogoutView,
    AssetAssignmentViewSet
)

# Define your urlpatterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # Ensure router is correctly defined
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    path('api/auth/login/', LoginView.as_view(), name='login'),
    path('api/password_reset/', PasswordResetView.as_view({'post': 'create'}), name='password-reset-request'),
    path('api/reset-password-confirm/', PasswordResetConfirmView.as_view(), name='reset-password-confirm'),
    path('api/auth/logout/', LogoutView.as_view(), name='logout'),
    path('api/auth/change_password/', PasswordChangeView.as_view(), name='change_password'),
    path('api/profile/update/', ProfileUpdateView.as_view(), name='profile-update'),
    path('api/tests/', Test.as_view(), name='tests'),
    path('api/assets/detail/<int:id>/', AssetDetailView.as_view(), name='asset_detail'),
]
