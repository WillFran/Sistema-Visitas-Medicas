# apps/doctores/models.py

from django.db import models
from django.conf import settings

from apps.productos.models import Producto
from apps.ubicaciones.models import Distrito


class Especialidad(models.Model):
    """
    Catálogo de especialidades médicas.
    A futuro se puede alinear con el catálogo oficial del CMP.
    """
    nombre = models.CharField(
        max_length=150,
        unique=True,
        help_text="Nombre de la especialidad médica (ej. Pediatría, Cardiología)."
    )
    codigo_cmp = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        help_text="Código oficial de la especialidad según CMP, si aplica."
    )

    class Meta:
        verbose_name = "Especialidad médica"
        verbose_name_plural = "Especialidades médicas"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Doctor(models.Model):
    cmp = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Número de CMP",
        help_text="Código de colegiatura según el Colegio Médico del Perú."
    )
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)

    # Campo legacy (texto)
    especialidad = models.CharField(
        max_length=100,
        help_text="Especialidad declarada. A futuro se normalizará con la tabla Especialidad."
    )

    # NUEVO: campo normalizado que apunta al catálogo Especialidad
    especialidad_fk = models.ForeignKey(
        Especialidad,
        on_delete=models.SET_NULL,
        related_name="doctores",
        null=True,
        blank=True,
        verbose_name="Especialidad",
        help_text="Especialidad médica normalizada (catálogo de Especialidades)."
    )

    direccion = models.TextField()
    fecha_nacimiento = models.DateField(null=True, blank=True)

    # Clasificación interna de importancia/prioridad del médico.
    CATEGORIAS = (
        (1, "Alta prioridad"),
        (2, "Prioridad media"),
        (3, "Baja prioridad"),
    )
    categoria = models.IntegerField(
        null=True,
        blank=True,
        choices=CATEGORIAS,
        help_text="Clasificación interna para segmentación comercial."
    )

    ubigeo = models.ForeignKey(
        Distrito,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="doctores",
        help_text="Distrito de atención principal del médico (UBIGEO oficial INEI)."
    )

    visitador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='doctores_asignados',
        null=True,
        blank=True,
        help_text="Visitador responsable asignado a este médico."
    )

    # Estado de habilitación CMP (gestionado manualmente por ahora)
    ESTADO_CMP = (
        ("habilitado", "Habilitado"),
        ("no_habilitado", "No habilitado"),
        ("suspendido", "Suspendido"),
    )
    estado_cmp = models.CharField(
        max_length=20,
        choices=ESTADO_CMP,
        default="habilitado",
        help_text="Estado de habilitación según CMP (actualizado manualmente en este sistema)."
    )

    # Auditoría básica
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Médico"
        verbose_name_plural = "Médicos"
        ordering = ["apellido", "nombre"]

    def __str__(self):
        return f"{self.apellido} {self.nombre} ({self.cmp})"


class Prescripcion(models.Model):
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name='prescripciones'
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name='prescripciones'
    )

    rank_tam = models.PositiveIntegerField(
        verbose_name="Ranking por Tamaño de Mercado"
    )
    ms_tam = models.FloatField(
        verbose_name="Market Share por Tamaño"
    )
    rank_trim = models.PositiveIntegerField(
        verbose_name="Ranking Trimestral"
    )
    ms_trim = models.FloatField(
        verbose_name="Market Share Trimestral"
    )

    fecha_registro = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Prescripción"
        verbose_name_plural = "Prescripciones"
        unique_together = ('doctor', 'producto')
        ordering = ["-fecha_registro"]

    def __str__(self):
        return f"{self.doctor} - {self.producto}"