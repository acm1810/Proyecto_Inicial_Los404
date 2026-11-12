import unicodedata
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Lugar, Categoria, Zona

def quitar_tildes(texto):
    """
    Función auxiliar para normalizar texto:
    Convierte 'Valparaíso' -> 'valparaiso' para comparar sin importar tildes ni mayúsculas.
    """
    if not texto:
        return ""
    texto_norm = unicodedata.normalize('NFD', texto)
    texto_sin_tildes = ''.join(c for c in texto_norm if unicodedata.category(c) != 'Mn')
    return texto_sin_tildes.lower().strip()


def inicio(request):
    """
    Funcionalidad Corazón:
    - Entrada: Búsqueda por texto (q) y filtrado por categoría/zona desde GET.
    - Búsqueda flexible: Ignora tildes, mayúsculas y minúsculas.
    - Redirección: Si escriben o eligen una Zona, redirige a zona.html.
    - Salida: Renderizado dinámico de la lista de lugares filtrados.
    """
    query = request.GET.get('q', '').strip()
    categoria_id = request.GET.get('categoria', '')
    zona_id = request.GET.get('zona', '')

    # 1. Redirección por selector de Zona
    if zona_id:
        return redirect('zona', id=int(zona_id))

    query_limpia = quitar_tildes(query)

    # 2. Verificar si el texto ingresado coincide con el NOMBRE DE UNA ZONA (sin importar tildes/mayúsculas)
    if query_limpia:
        zonas_todas = Zona.objects.all()
        for z in zonas_todas:
            if quitar_tildes(z.nombre) == query_limpia:
                return redirect('zona', id=z.id)

    lugares = Lugar.objects.all()
    categorias = Categoria.objects.all()
    zonas = Zona.objects.all().order_by('orden')

    # 3. Filtrar por CATEGORÍA si seleccionaron una en el dropdown
    if categoria_id:
        lugares = lugares.filter(categoria_id=categoria_id)

    # 4. Búsqueda flexible por TEXTO en Lugares y Categorías (sin importar tildes ni mayúsculas)
    if query_limpia:
        ids_coincidentes = []
        for lugar in lugares:
            nombre_lugar = quitar_tildes(lugar.nombre)
            desc_lugar = quitar_tildes(lugar.descripcion)
            comuna_lugar = quitar_tildes(getattr(lugar, 'comuna', ''))
            cat_lugar = quitar_tildes(lugar.categoria.nombre) if lugar.categoria else ''

            # Si la búsqueda coincide con el nombre, descripción, comuna o categoría del lugar
            if (query_limpia in nombre_lugar or 
                query_limpia in desc_lugar or 
                query_limpia in comuna_lugar or 
                query_limpia in cat_lugar):
                ids_coincidentes.append(lugar.id)

        lugares = Lugar.objects.filter(id__in=ids_coincidentes)
    elif not categoria_id:
        # Si no hay texto ni categoría seleccionada, mantenemos la lista limpia sin forzar resultados
        lugares = Lugar.objects.none()

    context = {
        'lugares': lugares,
        'categorias': categorias,
        'zonas': zonas,
        'query': query,
        'categoria_id': str(categoria_id),
        'zona_id': str(zona_id),
        'total_resultados': lugares.count() if (query or categoria_id) else 0
    }
    return render(request, 'lugares/inicio.html', context)


def zona(request, id):
    zona_obj = get_object_or_404(Zona, id=id)
    lugares = Lugar.objects.filter(zona=zona_obj)
    categorias = Categoria.objects.all()
    
    # !!! EL ARREGLO MAESTRO !!!
    if zona_obj.comunas:
        comunas = sorted([c.strip() for c in zona_obj.comunas.split(",") if c.strip()])
    else:
        comunas = []
    
    elegida = request.GET.get("categoria")
    if elegida:
        lugares = lugares.filter(categoria__id=elegida)
        
    texto = request.GET.get("q")
    if texto:
        texto_limpio = quitar_tildes(texto)
        ids_filtrados = []
        for l in lugares:
            if (texto_limpio in quitar_tildes(l.nombre) or 
                texto_limpio in quitar_tildes(l.descripcion) or 
                texto_limpio in quitar_tildes(getattr(l, 'comuna', ''))):
                ids_filtrados.append(l.id)
        lugares = lugares.filter(id__in=ids_filtrados)
        
    comuna = request.GET.get("comuna")
    if comuna:
        comuna_limpia = quitar_tildes(comuna)
        ids_comuna = [l.id for l in lugares if comuna_limpia in quitar_tildes(getattr(l, 'comuna', ''))]
        lugares = lugares.filter(id__in=ids_comuna)
        
    return render(request, "lugares/zona.html", {
        "zona": zona_obj, 
        "lugares": lugares, 
        "categorias": categorias,
        "elegida": elegida, 
        "comunas": comunas,
        "zonas": Zona.objects.all().order_by('orden'),
    })


def lugar_detalle(request, pk):
    lugar = get_object_or_404(Lugar, pk=pk)
    return render(request, 'lugares/lugar.html', {'lugar': lugar})