# apps/ubicaciones/models.py
from django.db import models


class Departamento(models.Model):
    ubigeo = models.CharField(
        max_length=2,
        unique=True,
        null=True,     # 👈 PERMITIR VACÍO SOLO PARA LA PRIMERA MIGRACIÓN
        blank=True,
        help_text="Código UBIGEO INEI (2 dígitos)"
    )
    nombre = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.nombre}"


class Provincia(models.Model):
    ubigeo = models.CharField(
        max_length=4,
        unique=True,
        null=True,     # 👈 PERMITIR VACÍO SOLO PARA LA PRIMERA MIGRACIÓN
        blank=True,
        help_text="Código UBIGEO INEI (4 dígitos)"
    )
    nombre = models.CharField(max_length=100)
    departamento = models.ForeignKey(
        Departamento,
        on_delete=models.PROTECT,   # 👈 NO DEJAR BORRAR UBIGEO
        related_name="provincias"
    )

    class Meta:
        verbose_name = "Provincia"
        verbose_name_plural = "Provincias"
        ordering = ["departamento__nombre", "nombre"]
        unique_together = ("nombre", "departamento")

    def __str__(self):
        return f"{self.nombre} — {self.departamento.nombre}"


class Distrito(models.Model):
    ubigeo = models.CharField(
        max_length=6,
        unique=True,
        null=True,      # 👈 PERMITIR VACÍO SOLO PARA LA PRIMERA MIGRACIÓN
        blank=True,
        help_text="Código UBIGEO INEI (6 dígitos)"
    )
    nombre = models.CharField(max_length=150)
    provincia = models.ForeignKey(
        Provincia,
        on_delete=models.PROTECT,
        related_name="distritos"
    )

    class Meta:
        verbose_name = "Distrito"
        verbose_name_plural = "Distritos"
        ordering = [
            "provincia__departamento__nombre",
            "provincia__nombre",
            "nombre"
        ]
        unique_together = ("nombre", "provincia")

    def __str__(self):
        return f"{self.nombre} — {self.provincia.nombre} / {self.provincia.departamento.nombre}"