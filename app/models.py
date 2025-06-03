from django.db import models

# Create your models here.
class producto(models.Model):
    idproducto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=350)
    descripcion = models.CharField(max_length=2500)
    iEstado = models.IntegerField(default=1)
