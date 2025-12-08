# apps/doctores/admin.py
from django.contrib import admin
from .models import Doctor, Especialidad, Prescripcion


@admin.register(Especialidad)
class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ("nombre", "codigo_cmp")
    search_fields = ("nombre", "codigo_cmp")
    ordering = ("nombre",)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = (
        "cmp",
        "apellido",
        "nombre",
        "especialidad_fk",   # 👈 mostramos la especialidad normalizada
        "ubigeo",
        "visitador",
        "estado_cmp",
        "creado_en",
    )

    search_fields = (
        "cmp",
        "nombre",
        "apellido",
        "especialidad",            # texto legacy (por si necesitas buscarlo)
        "especialidad_fk__nombre", # catálogo normalizado
    )

    # Ahora usamos el filtro por FK en lugar del filtro de texto
    list_filter = ("especialidad_fk", "estado_cmp", "visitador")

    autocomplete_fields = ("ubigeo", "visitador")
    ordering = ("apellido", "nombre")

    # Dejamos el campo de texto como legacy (solo lectura) para no seguirlo tocando
    readonly_fields = ("especialidad",)

    fieldsets = (
        ("Información principal", {
            "fields": (
                "cmp",
                "nombre",
                "apellido",
                "especialidad_fk",   # 👈 selección desde catálogo
                "especialidad",      # 👈 texto legacy solo lectura
                "estado_cmp",
            )
        }),
        ("Información de ubicación", {
            "fields": ("direccion", "ubigeo")
        }),
        ("Datos adicionales", {
            "fields": ("fecha_nacimiento", "categoria", "visitador")
        }),
    )


@admin.register(Prescripcion)
class PrescripcionAdmin(admin.ModelAdmin):
    list_display = ("doctor", "producto", "rank_tam", "rank_trim", "fecha_registro")
    search_fields = ("doctor__nombre", "doctor__apellido", "producto__nombre")
    autocomplete_fields = ("doctor", "producto")
    ordering = ("doctor",)