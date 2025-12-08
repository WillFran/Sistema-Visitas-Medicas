# apps/productos/models.py
from django.db import models


class Producto(models.Model):
    """
    Catálogo de productos farmacéuticos y materiales asociados
    usados en el sistema de visitas médicas.
    """

    # Clasificación del producto según su uso en visita
    TIPO_CHOICES = [
        ('prescribible', 'Medicamento de Prescripción (RX)'),
        ('muestra', 'Muestra Médica'),
        ('promocional', 'Material Promocional'),
        ('merch', 'Merchandising Institucional'),
    ]

    # -----------------------------
    # Identificación
    # -----------------------------
    codigo_interno = models.CharField(
        max_length=50,
        unique=True,
        null=True,
        blank=True,
        help_text="Código interno Diphasac o del laboratorio."
    )

    # 'nombre' existed antes: lo usamos como nombre comercial
    nombre = models.CharField(
        "Nombre comercial",
        max_length=150,
        help_text="Nombre comercial del producto (ej. Nayflex, Ibucalm)."
    )

    # -----------------------------
    # Información farmacéutica
    # -----------------------------
    dci = models.CharField(
        "Denominación común internacional (DCI)",
        max_length=150,
        null=True,
        blank=True,
        help_text="Principio(s) activo(s) en DCI, ej. Ibuprofeno."
    )

    forma_farmaceutica = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Forma farmacéutica: comprimidos, cápsulas, suspensión oral, etc."
    )

    concentracion = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Concentración: ej. 400 mg, 100 mg/5 mL, 500 mg + 65 mg."
    )

    presentacion = models.CharField(
        max_length=150,
        help_text="Ej. Caja x 10 blíster x 10 comprimidos; frasco x 150 mL."
    )

    categoria = models.CharField(
        "Categoría terapéutica",
        max_length=150,
        blank=True,
        help_text="Grupo terapéutico interno (ej. Analgésico, AINE, Antipirético)."
    )

    codigo_atc = models.CharField(
        max_length=20,
        blank=True,
        help_text="Código ATC oficial (ej. M01AE01 para ibuprofeno)."
    )

    gtin = models.CharField(
        max_length=20,
        blank=True,
        help_text="Código de barras / GTIN (EAN-13/14), si aplica."
    )

    # -----------------------------
    # Clasificación para el sistema
    # -----------------------------
    tipo_producto = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        default='prescribible',
        help_text="Clasificación del producto según su uso en visita médica."
    )

    activo = models.BooleanField(
        default=True,
        help_text="Indica si el producto está disponible para selección en el sistema."
    )

    creado_en = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    actualizado_en = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ["nombre"]

    def __str__(self):
        # Ejemplo: "Nayflex (Ibuprofeno 400 mg)"
        if self.dci and self.concentracion:
            return f"{self.nombre} ({self.dci} {self.concentracion})"
        return self.nombre