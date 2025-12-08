# apps/ubicaciones/admin.py

from django.contrib import admin
from .models import Departamento, Provincia, Distrito


@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ("ubigeo", "nombre")
    search_fields = ("ubigeo", "nombre")
    ordering = ("nombre",)


@admin.register(Provincia)
class ProvinciaAdmin(admin.ModelAdmin):
    list_display = ("ubigeo", "nombre", "departamento")
    search_fields = ("ubigeo", "nombre", "departamento__nombre")
    list_filter = ("departamento",)
    ordering = ("departamento__nombre", "nombre")


@admin.register(Distrito)
class DistritoAdmin(admin.ModelAdmin):
    list_display = ("ubigeo", "nombre", "provincia", "departamento")
    search_fields = (
        "ubigeo",
        "nombre",
        "provincia__nombre",
        "provincia__departamento__nombre",
    )
    list_filter = ("provincia__departamento", "provincia")
    ordering = ("provincia__departamento__nombre", "provincia__nombre", "nombre")

    @admin.display(ordering="provincia__departamento__nombre", description="Departamento")
    def departamento(self, obj):
        if obj.provincia and obj.provincia.departamento:
            return obj.provincia.departamento.nombre
        return ""