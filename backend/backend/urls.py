# backend/urls.py
from webbrowser import get
from django.contrib import admin
from django.urls import path, include
from assets import views
from routers import router  # Import router from the root directory
from assets.tests import Test
from assets.viewsets import(
 AssetDetailView, RegisterView, LoginView, LogoutView, PasswordResetView, AssetAssignmentViewSet
)
# Define your urlpatterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    path('api/auth/login/', LoginView.as_view(), name='login'),
    path('api/auth/logout/', LogoutView.as_view(), name='logout'),
    path('api/auth/reset_password/', PasswordResetView.as_view(), name='reset_password'),
    path('api/tests/', Test.as_view(), name="tests"),
    path('api/assets/detail/<int:id>/', AssetDetailView.as_view(), name='asset_detail'),
]
