# 🌈 RainbowKids — Sistema de Gestión para Guardería Infantil

RainbowKids es un sitio web desarrollado para gestionar consultas e inscripciones realizadas por padres de niños entre 2 y 5 años.  
Incluye un sistema de autenticación seguro, envío de correos de validación, panel administrativo con estadísticas y consumo de una API externa.

Este proyecto fue desarrollado utilizando Django, PostgreSQL y Django REST Framework como parte del Segundo Parcial de Programación Web 2.

---

## Funcionalidades Principales

### Formulario de Inscripción
- Validado con **Django Forms** + **JavaScript**
- Guarda la información en **PostgreSQL**
- Envía correo automático de confirmación al tutor

### Autenticación y Registro Seguro
- Registro limitado solo a correos permitidos (modelo `AllowedUser`)
- Envío de **código de validación por email**
- Activación de cuenta antes del login
- Inicio y cierre de sesión
- Formularios en español

### Dashboard Administrativo
- Accesible solo a usuarios validados
- Visualización de todas las solicitudes
- Estadísticas:
  - Total de consultas
  - Consultas por categoría (comercial, técnica, RRHH, general)
- Posibilidad de eliminar solicitudes

### API Externa Integrada
- Se consume información del clima usando **Open-Meteo**
- Se muestra en la página de inscripción junto a un iframe del mapa de la guardería

### API Interna (DRF)
- Endpoint `/api/consultas/` para obtener todas las solicitudes en JSON

---

## Tecnologías Utilizadas

- **Django 5.2.8**
- **Django REST Framework**
- **PostgreSQL**
- **Bootstrap 5**
- **JavaScript**
- **Open-Meteo API**

---

## Instalación y Ejecución

### 1️⃣ Crear entorno virtual

```bash
python -m venv venv
venv\Scripts\activate    # Windows
source venv/bin/activate # Linux/Mac
```

### 2️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3️⃣ Configurar variables de entorno

Crear un archivo `.env` con:

```
DB_NAME=rainbowkids_db
DB_USER=postgres
DB_PASSWORD=TU_PASSWORD
DB_HOST=localhost
DB_PORT=5432

EMAIL_HOST=c2280296.ferozo.com
EMAIL_PORT=465
EMAIL_USER=TU_CORREO
EMAIL_PASSWORD=TU_PASSWORD
```

⚠️ **No subir este archivo al repositorio.**

### 4️⃣ Aplicar migraciones

```bash
python manage.py migrate
```

### 5️⃣ Ejecutar servidor local

```bash
python manage.py runserver
```

Ir a:  
👉 http://127.0.0.1:8000/

---

## 🗄 Configuración de la Base de Datos (PostgreSQL)

En `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
    }
}
```

---

## Configuración del Servidor de Correo

```python
EMAIL_BACKEND = 'web_app.email_backend.UnverifiedSSLBackend'

EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = os.environ.get("EMAIL_PORT")
EMAIL_USE_SSL = True
EMAIL_USE_TLS = False

EMAIL_HOST_USER = os.environ.get("EMAIL_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_PASSWORD")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
```

---

## API Externa — Open-Meteo

URL utilizada:

```
https://api.open-meteo.com/v1/forecast?latitude=-34.6037&longitude=-58.3816&current_weather=true&hourly=precipitation_probability
```

Información mostrada:
- Estado del clima  
- Temperatura  
- Viento  
- Probabilidad de lluvia  

---

## Endpoints Internos

### 👉 API de Consultas
`GET /api/consultas/`  
Retorna todas las solicitudes en formato JSON (requiere login).

### 👉 API del Formulario
`POST /api/inscripcion/`  
Recibe la inscripción vía AJAX y almacena los datos.

---

## Acceso al Panel Administrativo

### 1️⃣ Registro  
👉 `/register/`  
Solo se aceptan correos incluidos en `AllowedUser`.

### 2️⃣ Validación de Cuenta  
Se enviará un código por mail.  
👉 `/validar_cuenta/`

### 3️⃣ Login  
👉 `/login/`

### 4️⃣ Dashboard  
👉 `/dashboard/`  
(Requiere usuario validado)

---

## Superusuario (solo local)

```bash
python manage.py createsuperuser
```

---

## Notas Importantes

- Los usuarios se crean como **inactivos** hasta validar su código.
- El dashboard está protegido con `login_required`.
- Se evita registrar correos no autorizados.
- Todas las vistas públicas están separadas de las de autenticación.
- El envío de mails se prueba en local (Render no lo permite sin extras).

---

# Estado Final del Proyecto

✔ Backend completo  
✔ Autenticación funcionando  
✔ Envío de correos activo  
✔ Dashboard con estadísticas  
✔ API interna + API externa  
✔ Validación de usuarios permitidos  
✔ Base de datos en PostgreSQL  
