from django.shortcuts import render

# Create your views here.
from .models import Zona

def inicio(request):
    zonas = Zona.objects.all()
    return render(request, "lugares/inicio.html", {"zonas": zonas})
