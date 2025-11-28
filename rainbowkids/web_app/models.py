from django.db import models

# Create your models here.
class ParentInquiry(models.Model):
    CATEGORIAS = [
        ('vacantes', 'Vacantes / Inscripciones'),
        ('general', 'Consulta General'),
        ('salud', 'Salud / Alergias'),
        ('horario', 'Horario / Jornada'),
        ('comercial', 'Comercial / Precios'),
    ]

    # Datos del tutor
    tutor_nombre = models.CharField(max_length=100)
    tutor_apellido = models.CharField(max_length=100)
    tutor_email = models.EmailField()
    tutor_telefono = models.CharField(max_length=30, blank=True, null=True)

    # Datos del niño
    ninio_nombre = models.CharField(max_length=100)
    ninio_apellido = models.CharField(max_length=100)
    ninio_edad = models.IntegerField()  # validaremos 2–5 años en el form

    # Comentarios opcionales
    comentario = models.TextField(blank=True, null=True)

    # Categoría asignada automáticamente
    categoria = models.CharField(
        max_length=20,
        choices=CATEGORIAS,
        default='general'
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tutor_nombre} {self.tutor_apellido} - {self.ninio_nombre}"


class AllowedUser(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    codigo_validacion = models.CharField(max_length=20)
    registrado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.email}"
