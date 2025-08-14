from django.contrib import admin
from django.urls import path, include           # <- OJO: include importado
from home.views import home

urlpatterns = [
    path("", home, name="home"),                # /
    path("admin/", admin.site.urls),            # /admin/
    path("indicadores/", include("indicadores.urls")),  # /indicadores/...
]
