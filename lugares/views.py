import unicodedata
from urllib.parse import urlencode
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.db.models import Q
from .models import Lugar, Categoria, Zona

def quitar_tildes(texto):
    if not texto:
        return ""
    texto_norm = unicodedata.normalize('NFD', texto)
    return ''.join(c for c in texto_norm if unicodedata.category(c) != 'Mn').lower().strip()

def inicio(request):
    query = request.GET.get('q', '').strip()
    categoria_id = request.GET.get('categoria', '').strip()
    zona_id = request.GET.get('zona', '').strip()

    # 1. Redirección por selector de Zona conservando categoría/texto
    if zona_id:
        url = reverse('zona', kwargs={'id': int(zona_id)})
        params = {}
        if categoria_id:
            params['categoria'] = categoria_id
        if query:
            params['q'] = query
        if params:
            url = f"{url}?{urlencode(params)}"
        return redirect(url)

    query_limpia = quitar_tildes(query)

    # 2. Redirección por texto si coincide con una Zona conservando categoría
    if query_limpia:
        zonas_todas = Zona.objects.all()
        for z in zonas_todas:
            if quitar_tildes(z.nombre) == query_limpia:
                url = reverse('zona', kwargs={'id': z.id})
                if categoria_id:
                    url = f"{url}?{urlencode({'categoria': categoria_id})}"
                return redirect(url)

    lugares = Lugar.objects.all()
    categorias = Categoria.objects.all()
    zonas = Zona.objects.all().order_by('orden')

    if categoria_id:
        lugares = lugares.filter(categoria_id=categoria_id)

    if query_limpia:
        ids_coincidentes = []
        for lugar in lugares:
            if (query_limpia in quitar_tildes(lugar.nombre) or 
                query_limpia in quitar_tildes(lugar.descripcion) or 
                query_limpia in quitar_tildes(getattr(lugar, 'comuna', '')) or 
                query_limpia in quitar_tildes(lugar.categoria.nombre if lugar.categoria else '')):
                ids_coincidentes.append(lugar.id)
        lugares = Lugar.objects.filter(id__in=ids_coincidentes)
    elif not categoria_id:
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
    
    comunas = sorted([c.strip() for c in zona_obj.comunas.split(",") if c.strip()]) if zona_obj.comunas else []
    
    elegida = request.GET.get("categoria")
    if elegida:
        lugares = lugares.filter(categoria__id=elegida)
        
    texto = request.GET.get("q")
    if texto:
        texto_limpio = quitar_tildes(texto)
        ids_filtrados = [l.id for l in lugares if (texto_limpio in quitar_tildes(l.nombre) or texto_limpio in quitar_tildes(l.descripcion))]
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