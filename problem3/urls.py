from django.contrib import admin
from django.urls import path, include
from . import settings
from django.conf.urls import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('project.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_url=settings.STATIC_ROOT)
