from django.urls import path
from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("zona/<int:id>/", views.zona, name="zona"),
    path("lugar/<int:id>/", views.lugar, name="lugar"), 
]