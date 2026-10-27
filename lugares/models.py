from django.db import models

class Zona(models.Model):
    nombre = models.CharField(max_length=80)
    frase = models.CharField(max_length=80, blank=True)
    comunas = models.CharField(max_length=200, blank=True)
    descripcion = models.TextField(blank=True)
    orden = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    class Meta:
        verbose_name = "categoría"
        verbose_name_plural = "categorías"
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Lugar(models.Model):
    class Meta:
        verbose_name_plural = "lugares"
    nombre = models.CharField(max_length=120)
    zona = models.ForeignKey(Zona, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    comuna = models.CharField(max_length=60)
    resumen = models.CharField(max_length=200)
    descripcion = models.TextField()
    direccion = models.CharField(max_length=200, blank=True)
    horario = models.CharField(max_length=200, blank=True)
    precio = models.CharField(max_length=200, blank=True)
    contacto = models.CharField(max_length=200, blank=True)
    sitio_web = models.URLField(blank=True)
    fuente = models.URLField(blank=True)
    como_llegar = models.TextField(blank=True)
    revisado = models.DateField(null=True, blank=True)
    destacado = models.BooleanField(default=False)
    imagen = models.ImageField(upload_to="lugares/", blank=True)

    def __str__(self):
        return self.nombre
