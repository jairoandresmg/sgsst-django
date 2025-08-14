from django import forms
from .models import RegistroMensual

class RegistroMensualForm(forms.ModelForm):
    class Meta:
        model = RegistroMensual
        fields = "__all__"

    def clean(self):
        cleaned = super().clean()
        # llama a las validaciones del modelo
        self.instance.__dict__.update(cleaned)
        self.instance.clean()
        return cleaned
