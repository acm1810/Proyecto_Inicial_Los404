from django.shortcuts import render, get_object_or_404
from .models import Lugar, Categoria, Zona

def inicio(request):
    """
    Funcionalidad Corazón:
    - Entrada: Búsqueda por texto (q) y filtrado por categoría/zona desde GET.
    - Procesamiento: Filtrado en la base de datos SQLite con consultas condicionales.
    - Salida: Renderizado dinámico de la lista de lugares filtrados.
    """
    query = request.GET.get('q', '').strip()
    categoria_id = request.GET.get('categoria', '')
    zona_id = request.GET.get('zona', '')

    lugares = Lugar.objects.all()
    categorias = Categoria.objects.all()
    zonas = Zona.objects.all().order_by('orden')

    # Filtrado dinámico según parámetros de entrada
    if query:
        lugares = lugares.filter(nombre__icontains=query) | lugares.filter(descripcion__icontains=query)
    if categoria_id:
        lugares = lugares.filter(categoria_id=categoria_id)
    if zona_id:
        lugares = lugares.filter(zona_id=zona_id)

    context = {
        'lugares': lugares,
        'categorias': categorias,
        'zonas': zonas,
        'query': query,
        'categoria_id': str(categoria_id),
        'zona_id': str(zona_id),
        'total_resultados': lugares.count()
    }
    return render(request, 'lugares/inicio.html', context)

def lugar_detalle(request, pk):
    lugar = get_object_or_404(Lugar, pk=pk)
    return render(request, 'lugares/lugar.html', {'lugar': lugar})
