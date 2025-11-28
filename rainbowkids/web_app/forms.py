from django import forms
from django.contrib.auth.forms import User

class InscripcionForm(forms.Form):

    # Datos del Niño/a
    ninio_nombre = forms.CharField(
        label="Nombre del niño/a:",
        max_length=50,
        min_length=2,
        required=True,
        error_messages={
            "required": "Por favor ingresá el nombre del niño/a.",
            "min_length": "El nombre es demasiado corto.",
            "max_length": "El nombre es demasiado largo.",
        }
    )

    ninio_apellido = forms.CharField(
        label="Apellido del niño/a:",
        max_length=50,
        min_length=2,
        required=True,
        error_messages={
            "required": "Por favor ingresá el apellido del niño/a.",
            "min_length": "El apellido es demasiado corto.",
            "max_length": "El apellido es demasiado largo.",
        }
    )

    ninio_edad = forms.IntegerField(
        label="Edad:",
        min_value=2,
        max_value=5,
        required=True,
        error_messages={
            "required": "Ingresá la edad.",
            "min_value": "La edad mínima es 2 años.",
            "max_value": "La edad máxima es 5 años.",
        }
    )

    # Datos del Tutor
    tutor_nombre = forms.CharField(
        label="Nombre del tutor:",
        max_length=50,
        required=True,
        error_messages={
            "required": "Ingresá el nombre del padre/madre/tutor."
        }
    )

    tutor_apellido = forms.CharField(
        label="Apellido del tutor:",
        max_length=50,
        required=True,
        error_messages={
            "required": "Ingresá el apellido del padre/madre/tutor."
        }
    )

    tutor_email = forms.EmailField(
        label="Email de contacto:",
        required=True,
        error_messages={
            "required": "Ingresá un correo electrónico.",
            "invalid": "El correo no tiene un formato válido.",
        }
    )

    tutor_telefono = forms.RegexField(
        label="Teléfono:",
        regex=r'^\+?\d{7,15}$',
        required=False,
        error_messages={
            "invalid": "El número de teléfono debe contener solo dígitos (7-15)."
        }
    )

    comentario = forms.CharField(
        label="Comentarios (alergias, información importante):",
        widget=forms.Textarea,
        required=False
    )

class RegistroForm(forms.Form):
    nombre = forms.CharField(max_length=50)
    apellido = forms.CharField(max_length=50)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)