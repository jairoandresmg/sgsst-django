from django.contrib import admin
from django.urls import path, include
from home.views import home

urlpatterns = [
    path("", home, name="home"),                     # portada
    path("admin/", admin.site.urls),
    path("indicadores/", include("indicadores.urls"))  # monta las rutas de la app
]
