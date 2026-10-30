from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('lugares.urls')),  # Esto conecta tus archivos HTML con el proyecto entero
]

# Esto activa las fotos de Yutong en tus tarjetas
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
