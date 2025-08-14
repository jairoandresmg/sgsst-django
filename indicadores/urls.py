from django.urls import path
from .views import lista_registros, nuevo_registro, detalle_registro

urlpatterns = [
    path("", lista_registros, name="lista_registros"),
    path("nuevo/", nuevo_registro, name="nuevo_registro"),
    path("<int:pk>/", detalle_registro, name="detalle_registro"),
]
