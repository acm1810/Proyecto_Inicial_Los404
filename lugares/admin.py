from django.contrib import admin

# Register your models here.
from .models import Zona, Categoria, Lugar

admin.site.register(Zona)
admin.site.register(Categoria)
admin.site.register(Lugar)