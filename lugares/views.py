from django.shortcuts import render, get_object_or_404

# Create your views here.
from .models import Zona, Lugar

def inicio(request):
    zonas = Zona.objects.all()
    return render(request, "lugares/inicio.html", {"zonas": zonas})

def zona(request, id):
    zona = get_object_or_404(Zona, id=id)
    lugares = Lugar.objects.filter(zona=zona)
    return render(request, "lugares/zona.html", {"zona": zona, "lugares": lugares})

def lugar(request, id):
    lugar = get_object_or_404(Lugar, id=id)
    return render(request, "lugares/lugar.html", {"lugar": lugar})
