from django.db import models

class RegistroMensual(models.Model):
    anio = models.PositiveIntegerField()
    mes = models.PositiveSmallIntegerField()  # 1-12
    dias_laborables = models.PositiveSmallIntegerField(default=0)

    hh_programadas = models.PositiveIntegerField(default=0)
    hh_realizadas  = models.PositiveIntegerField(default=0)

    simulacros_prog = models.PositiveSmallIntegerField(default=0)
    simulacros_real = models.PositiveSmallIntegerField(default=0)

    inspecciones_prog = models.PositiveSmallIntegerField(default=0)
    inspecciones_real = models.PositiveSmallIntegerField(default=0)

    dias_perdidos_acc = models.PositiveIntegerField(default=0)
    dias_cargados_mes  = models.PositiveIntegerField(default=0)

    accidentes = models.PositiveSmallIntegerField(default=0)
    accidentes_mortales = models.PositiveSmallIntegerField(default=0)

    casos_enf_nuevos = models.PositiveSmallIntegerField(default=0)
    casos_enf_antiguos = models.PositiveSmallIntegerField(default=0)

    trabajadores_prom = models.FloatField(default=0)
    dias_incapacidad_total = models.PositiveIntegerField(default=0)
    dias_trabajo_programado = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('anio', 'mes')
        ordering = ['-anio','-mes']

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.accidentes_mortales > self.accidentes:
            raise ValidationError("Los accidentes mortales no pueden superar los accidentes totales.")
        if self.simulacros_real > self.simulacros_prog:
            raise ValidationError("Simulacros realizados no puede superar los programados.")
        if self.inspecciones_real > self.inspecciones_prog:
            raise ValidationError("Inspecciones realizadas no puede superar las programadas.")
        if (self.hh_programadas or self.hh_realizadas) and self.trabajadores_prom <= 0:
            raise ValidationError("Si hay horas hombre, 'trabajadores_prom' debe ser > 0.")

    # Cálculos básicos (como en tu Excel)
    def indicadores(self):
        hh = max(self.hh_realizadas, 1)
        trabajadores_dias = max(self.trabajadores_prom * max(self.dias_laborables, 0), 1)

        severidad  = (self.dias_perdidos_acc / hh) * 1000
        frecuencia = (self.accidentes / hh) * 1_000_000
        mortalidad = (self.accidentes_mortales / max(self.accidentes, 1)) * 100
        prevalencia = (self.casos_enf_antiguos / max(self.trabajadores_prom, 1)) * 100
        incidencia  = (self.casos_enf_nuevos / max(self.trabajadores_prom, 1)) * 100
        ausentismo  = (self.dias_incapacidad_total / trabajadores_dias) * 100

        pct_hh = (self.hh_realizadas / max(self.hh_programadas, 1)) * 100
        pct_sim = (self.simulacros_real / max(self.simulacros_prog, 1)) * 100
        pct_insp = (self.inspecciones_real / max(self.inspecciones_prog, 1)) * 100

        return dict(
            severidad=severidad, frecuencia=frecuencia, mortalidad=mortalidad,
            prevalencia=prevalencia, incidencia=incidencia, ausentismo=ausentismo,
            pct_hh=pct_hh, pct_simulacros=pct_sim, pct_inspecciones=pct_insp
        )

    def __str__(self):
        return f"{self.anio}-{self.mes:02d}"
