from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import InscripcionForm, RegistroForm
from .models import ParentInquiry, AllowedUser
import json
from .utils import clasificar_consulta
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ParentInquirySerializer
import requests
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse



# PÁGINAS PÚBLICAS

def index(request):
    return render(request, 'web_app/index.html')

def actividades(request):
    return render(request, 'web_app/actividades.html')

def nosotros(request):
    return render(request, 'web_app/nosotros.html')

def inscripcion(request):
    form = InscripcionForm()
    clima = obtener_clima()
    return render(request, 'web_app/inscripcion.html', {'form': form, 'clima': clima})


# API FORMULARIO

@csrf_exempt
def inscripcion_api(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    data = json.loads(request.body.decode("utf-8"))
    form = InscripcionForm(data)

    if not form.is_valid():
        return JsonResponse({"success": False, "errors": form.errors}, status=400)

    consulta = ParentInquiry.objects.create(
        tutor_nombre=form.cleaned_data["tutor_nombre"],
        tutor_apellido=form.cleaned_data["tutor_apellido"],
        tutor_email=form.cleaned_data["tutor_email"],
        tutor_telefono=form.cleaned_data["tutor_telefono"],
        ninio_nombre=form.cleaned_data["ninio_nombre"],
        ninio_apellido=form.cleaned_data["ninio_apellido"],
        ninio_edad=form.cleaned_data["ninio_edad"],
        comentario=form.cleaned_data["comentario"],
        categoria=clasificar_consulta(form.cleaned_data["comentario"] or "")
    )

    # ============================================
    #  ENVÍO DE CORREO AL TUTOR
    # ============================================

    try:
        mensaje = (
            f"Hola {consulta.tutor_nombre},\n\n"
            "Recibimos tu solicitud de inscripción en RainbowKids.\n\n"
            f"Categoría asignada: {consulta.categoria}\n\n"
            "Datos enviados:\n"
            f"- Tutor: {consulta.tutor_nombre} {consulta.tutor_apellido}\n"
            f"- Email: {consulta.tutor_email}\n"
            f"- Teléfono: {consulta.tutor_telefono or 'No informado'}\n\n"
            f"- Niño/a: {consulta.ninio_nombre} {consulta.ninio_apellido}\n"
            f"- Edad: {consulta.ninio_edad}\n"
            f"- Comentarios: {consulta.comentario or 'Sin comentarios'}\n\n"
            "Gracias por contactarte con RainbowKids.\n"
            "Nos estaremos comunicando a la brevedad.\n"
        )

        send_mail(
            subject=f"Confirmación de inscripción - Categoría: {consulta.categoria}",
            message=mensaje,
            from_email="elena.gonzalez@lalupitacontenidos.site",  
            recipient_list=[consulta.tutor_email],
            fail_silently=False,
        )
    except Exception as e:
        # Si el email falla, registrar el error pero continuar
        print(f"⚠️  Error al enviar email: {e}")
        # La inscripción ya fue guardada
    
    # ============================================

    return JsonResponse({
        "success": True,
        "message": "Inscripción enviada correctamente.",
        "id": consulta.id
    })



# REGISTRO Y VALIDACIÓN

from django.core.mail import send_mail

def register(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]

            # Verificar si el correo está permitido
            try:
                allowed = AllowedUser.objects.get(email=email)
            except AllowedUser.DoesNotExist:
                return render(request, "web_app/register.html", {
                    "form": form,
                    "error": "Acceso restringido. No está autorizado a utilizar este sistema."
                })

            # Crear usuario INACTIVO hasta validar la cuenta
            user = User.objects.create_user(
                username=email,
                email=email,
                password=form.cleaned_data["password"],
                first_name=form.cleaned_data["nombre"],
                last_name=form.cleaned_data["apellido"],
                is_active=False
            )

            allowed.registrado = True
            allowed.save()

            # ========== ENVÍO DE EMAIL ==========
            try:
                codigo = allowed.codigo_validacion
                
                validacion_url = request.build_absolute_uri('/validar_cuenta/')

                mensaje = (
                    f"Hola {allowed.nombre},\n\n"
                    f"Gracias por registrarte en RainbowKids.\n\n"
                    f"Para validar tu cuenta, ingresá este código:\n\n"
                    f"🔐 Código de validación: {codigo}\n\n"
                    f"Validá tu cuenta aquí:\n"
                    f"{validacion_url}\n\n"
                    "Saludos,\nRainbowKids"
                )

                send_mail(
                    subject="Validación de cuenta - RainbowKids",
                    message=mensaje,
                    from_email="elena.gonzalez@lalupitacontenidos.site",
                    recipient_list=[email],
                    fail_silently=False,
                )
            except Exception as e:
                # Si el email falla, registrar el error pero continuar
                print(f"⚠️  Error al enviar email de validación: {e}")
                # El usuario ya fue creado, así que continuamos de todas formas

            return render(request, "web_app/validar_cuenta.html", {
                "email": email,
                "success": "Le llegará un correo para validar su cuenta."
            })

    else:
        form = RegistroForm()

    return render(request, "web_app/register.html", {"form": form})


def validar_cuenta(request):
    if request.method == "POST":
        email = request.POST.get("email")
        codigo = request.POST.get("codigo")

        try:
            allowed = AllowedUser.objects.get(email=email)
        except AllowedUser.DoesNotExist:
            return render(request, "web_app/validar_cuenta.html", {
                "error": "Email no encontrado."
            })

        if allowed.codigo_validacion == codigo:
            # activar usuario
            try:
                user = User.objects.get(username=email)
                user.is_active = True
                user.save()
            except User.DoesNotExist:
                return render(request, "web_app/validar_cuenta.html", {
                    "error": "No existe un usuario con este correo.",
                    "email": email
                })

            return render(request, "web_app/login.html", {
                "success": "Cuenta validada correctamente. Ya podés iniciar sesión."
            })

        # código incorrecto
        return render(request, "web_app/validar_cuenta.html", {
            "error": "Código incorrecto.",
            "email": email
        })

    return render(request, "web_app/validar_cuenta.html")


# Login / Logout
def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            return render(request, "web_app/login.html", {
                "error": "Email o contraseña incorrectos."
            })

    return render(request, "web_app/login.html")


def logout_view(request):
    logout(request)
    return redirect('login')


# Dashboard
@login_required
def dashboard(request):
    consultas = ParentInquiry.objects.all().order_by("-fecha_creacion")

    stats = {
        "vacantes": consultas.filter(categoria="vacantes").count(),
        "salud": consultas.filter(categoria="salud").count(),
        "comercial": consultas.filter(categoria="comercial").count(),
        "horario": consultas.filter(categoria="horario").count(),
        "general": consultas.filter(categoria="general").count(),
    }

    return render(request, "web_app/dashboard.html", {
        "consultas": consultas,
        "stats": stats,
        "total_consultas": consultas.count()
    })


@login_required
def eliminar_consulta(request, consulta_id):
    consulta = ParentInquiry.objects.get(id=consulta_id)
    consulta.delete()

    consultas = ParentInquiry.objects.all().order_by("-fecha_creacion")
    stats = {
        "vacantes": consultas.filter(categoria="vacantes").count(),
        "salud": consultas.filter(categoria="salud").count(),
        "comercial": consultas.filter(categoria="comercial").count(),
        "horario": consultas.filter(categoria="horario").count(),
        "general": consultas.filter(categoria="general").count(),
    }

    return render(request, "web_app/dashboard.html", {
        "consultas": consultas,
        "stats": stats,
        "success": "Consulta eliminada correctamente."
    })


# API de clima

@method_decorator(login_required, name='dispatch')
class ConsultasAPI(APIView):

    def get(self, request):
        consultas = ParentInquiry.objects.all().order_by("-fecha_creacion")
        serializer = ParentInquirySerializer(consultas, many=True)
        return Response(serializer.data)


def obtener_clima():
    try:
        lat = -34.6037
        lon = -58.3816

        url = (
            "https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}"
            "&current=temperature_2m,weather_code,precipitation_probability,"
            "wind_speed_10m"
        )

        response = requests.get(url)
        data = response.json()

        current = data["current"]

        weather_codes = {
            0: ("Cielo despejado", "☀️"),
            1: ("Mayormente despejado", "🌤️"),
            2: ("Parcialmente nublado", "⛅"),
            3: ("Nublado", "☁️"),
            45: ("Niebla", "🌫️"),
            51: ("Llovizna", "🌦️"),
            61: ("Lluvia ligera", "🌧️"),
            63: ("Lluvia moderada", "🌧️"),
            65: ("Lluvia fuerte", "🌧️"),
            80: ("Chaparrones", "🌧️"),
            95: ("Tormenta eléctrica", "⛈️"),
        }

        estado, icono = weather_codes.get(
            current["weather_code"],
            ("Condición desconocida", "❓")
        )

        return {
            "estado": estado,
            "icono": icono,
            "temperatura": current["temperature_2m"],
            "lluvia_prob": current.get("precipitation_probability", 0),
            "viento": current["wind_speed_10m"]
        }

    except:
        return None
