from django.urls import path
from . import views
from .views import (
    register, login_view, logout_view, validar_cuenta,
    dashboard, eliminar_consulta, ConsultasAPI
)

urlpatterns = [
    path('', views.index, name='index'),
    path('actividades/', views.actividades, name='actividades'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('inscripciones/', views.inscripcion, name='inscripcion'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('validar_cuenta/', validar_cuenta, name='validar_cuenta'),
    path("dashboard/", dashboard, name="dashboard"),
    path("dashboard/eliminar/<int:consulta_id>/", eliminar_consulta, name="eliminar_consulta"),
    path("api/consultas/", ConsultasAPI.as_view(), name="api_consultas"),
    path("api/inscripcion/", views.inscripcion_api, name="inscripcion_api"),
]