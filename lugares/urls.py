from django.urls import path
from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("lugar/<int:pk>/", views.lugar_detalle, name="lugar"),
]