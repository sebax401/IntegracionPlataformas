from django.db import models

# Create your models here.

class usuarios(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    primer_nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    correo = models.EmailField()
    telefono = models.IntegerField()

    def __str__(self):
        return f'{self.primer_nombre} {self.apellido}'    

class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    imagen = models.ImageField(upload_to='productos/', null = True)
    nombre_producto = models.CharField(max_length=50)
    descripcion = models.TextField()
    precio = models.IntegerField()
    tipo = models.IntegerField(default=0, choices=[
        (0, 'casco'),
        (1, 'guantes'),
        (2, 'lentes'),
        (3, 'destornillador'),
        (4, 'kit de herramientas'),
        (5, 'lijadora'),
        (6, 'llaves'),
        (7, 'martillo'),
        (8, 'sierra'),
        (9, 'taladro'),
        (10, 'acabados de piso'),
        (11, 'arena'),
        (12, 'barnices'),
        (13, 'cemento'),
        (14, 'ceramica'),
        (15, 'ladrillos'),
        (16, 'pintura'),
    ])
    categoria = models.IntegerField(default=0, choices=[
        (1, 'epp'),
        (2, 'herramientas'),
        (3, 'materiales basicos')
    ])
    stock = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.nombre_producto} - {self.descripcion}'
    
    