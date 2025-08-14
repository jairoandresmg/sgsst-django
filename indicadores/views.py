from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistroMensualForm
from .models import RegistroMensual

def nuevo_registro(request):
    if request.method == "POST":
        form = RegistroMensualForm(request.POST)
        if form.is_valid():
            obj = form.save()
            return redirect("detalle_registro", pk=obj.pk)
    else:
        form = RegistroMensualForm()
    return render(request, "indicadores/form.html", {"form": form})

def detalle_registro(request, pk):
    obj = get_object_or_404(RegistroMensual, pk=pk)
    return render(request, "indicadores/detalle.html", {"m": obj, "ind": obj.indicadores()})

def lista_registros(request):
    qs = RegistroMensual.objects.all()
    return render(request, "indicadores/lista.html", {"items": qs})
