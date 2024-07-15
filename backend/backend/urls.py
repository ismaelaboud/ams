from django.contrib import admin
from django.urls import path, include
from routers import router  # Import router from the root directory

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # Include the API routes from the router
]
