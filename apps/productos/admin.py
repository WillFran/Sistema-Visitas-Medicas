# apps/productos/admin.py
from django.contrib import admin
from .models import Producto


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = (
        "codigo_interno",
        "nombre",              # nombre comercial
        "dci",
        "forma_farmaceutica",
        "concentracion",
        "tipo_producto",
        "activo",
    )
    search_fields = (
        "codigo_interno",
        "nombre",              # nombre comercial
        "dci",
        "codigo_atc",
    )
    list_filter = (
        "tipo_producto",
        "activo",
        "categoria",           # categoría terapéutica interna
    )
    ordering = ("nombre",)

    fieldsets = (
        ("Identificación", {
            "fields": (
                "codigo_interno",
                "gtin",
                "activo",
            )
        }),
        ("Información comercial", {
            "fields": (
                "nombre",
                "presentacion",
                "categoria",
            )
        }),
        ("Información farmacéutica", {
            "fields": (
                "dci",
                "forma_farmaceutica",
                "concentracion",
                "codigo_atc",
            )
        }),
        ("Clasificación para visitas médicas", {
            "fields": (
                "tipo_producto",
            )
        }),
    )