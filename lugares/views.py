from django.shortcuts import render, get_object_or_404, redirect
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

    if zona_id:
        return redirect('zona', id=int(zona_id))

    lugares = Lugar.objects.all()
    categorias = Categoria.objects.all()
    zonas = Zona.objects.all().order_by('orden')

    if query:
        lugares = lugares.filter(nombre__icontains=query) | lugares.filter(descripcion__icontains=query)
    if categoria_id:
        lugares = lugares.filter(categoria_id=categoria_id)

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

def zona(request, id):
    zona = get_object_or_404(Zona, id=id)
    lugares = Lugar.objects.filter(zona=zona)
    categorias = Categoria.objects.all()
    
    # !!! EL ARREGLO MAESTRO !!!
    # En vez de sacar las comunas de los lugares, las sacamos del texto oficial de la Zona
    if zona.comunas:
        # Separa el texto por las comas, limpia los espacios y los ordena alfabéticamente
        comunas = sorted([c.strip() for c in zona.comunas.split(",") if c.strip()])
    else:
        comunas = []
    
    elegida = request.GET.get("categoria")
    if elegida:
        lugares = lugares.filter(categoria__id=elegida)
        
    texto = request.GET.get("q")
    if texto:
        lugares = lugares.filter(nombre__icontains=texto) | lugares.filter(resumen__icontains=texto)
        
    comuna = request.GET.get("comuna")
    if comuna:
        # Filtra de forma flexible por si hay diferencias de tildes
        if "valpara" in comuna.lower():
            lugares = lugares.filter(comuna__icontains="Valpara")
        else:
            lugares = lugares.filter(comuna__icontains=comuna)
        
    return render(request, "lugares/zona.html", {
        "zona": zona, 
        "lugares": lugares, 
        "categorias": categorias,
        "elegida": elegida, 
        "comunas": comunas,
        "zonas": Zona.objects.all().order_by('orden'),
    })

def lugar_detalle(request, pk):
    lugar = get_object_or_404(Lugar, pk=pk)
    return render(request, 'lugares/lugar.html', {'lugar': lugar})
