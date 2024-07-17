# backend/urls.py

from django.contrib import admin
from django.urls import path, include
from routers import router  # Import router from the root directory
from assets.viewsets import CategoryViewSet, RegisterView, LoginView, LogoutView, PasswordResetView

# Register CategoryViewSet with a unique basename, e.g., 'category-api'
router.register(r'categories', CategoryViewSet, basename='category-api')

# Define your urlpatterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # Include the API routes from the router
    path('api/auth/register/', RegisterView.as_view(), name='register'),  # Add user registration route
    path('api/auth/login/', LoginView.as_view(), name='login'),  # Add user login route
    path('api/auth/logout/', LogoutView.as_view(), name='logout'),  # Add user logout route
    path('api/auth/reset_password/', PasswordResetView.as_view(), name='reset_password'),  # Add password reset route
]
