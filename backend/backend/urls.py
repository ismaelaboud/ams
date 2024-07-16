# backend/urls.py

from django.contrib import admin
from django.urls import path, include
from routers import router  # Import router from the root directory
from assets.viewsets import RegisterView, LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # Include the API routes from the router
    path('api/register/', RegisterView.as_view(), name='register'),  # Add user registration route
    path('api/login/', LoginView.as_view(), name='login'),  # Add user login route
]
