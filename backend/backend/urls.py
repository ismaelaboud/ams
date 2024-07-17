# backend/urls.py

from django.contrib import admin
from django.urls import path, include
from routers import router  # Import router from the root directory
from assets.viewsets import RegisterView, LoginView,LogoutView,PasswordResetView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # Include the API routes from the router
    path('api/auth/register/', RegisterView.as_view(), name='register'),  # Add user registration route
    path('api/auth/login/', LoginView.as_view(), name='login'),  # Add user login route
    path('api/auth/logout/', LogoutView.as_view(), name='logout'),
    path('api/auth/reset_password/', PasswordResetView.as_view(), name='reset_password'),
]
