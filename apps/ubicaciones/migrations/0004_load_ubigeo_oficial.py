import csv
from pathlib import Path
from django.db import migrations


def load_ubigeo_oficial(apps, schema_editor):
    Departamento = apps.get_model("ubicaciones", "Departamento")
    Provincia = apps.get_model("ubicaciones", "Provincia")
    Distrito = apps.get_model("ubicaciones", "Distrito")

    # Ruta: apps/ubicaciones/data/ubigeo_peru_oficial.csv
    base_dir = Path(__file__).resolve().parent.parent  # .../ubicaciones/
    data_dir = base_dir / "data"
    csv_path = data_dir / "ubigeo_peru_oficial.csv"

    if not csv_path.exists():
        raise FileNotFoundError(f"No se encontró el archivo UBIGEO: {csv_path}")

    # 1) Limpiar datos previos (importante si ya cargaste ejemplos)
    Distrito.objects.all().delete()
    Provincia.objects.all().delete()
    Departamento.objects.all().delete()

    # 2) Leer CSV completo
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Diccionarios temporales
    departamentos = {}  # dep_code -> {"nombre": ..., "ubigeo": ...}
    provincias = {}     # prov_code -> {"nombre": ..., "ubigeo": ..., "dep_code": ...}
    distritos = []      # lista de dicts con info completa

    for row in rows:
        ubigeo6 = (row.get("ubigeo") or "").strip()
        dep_name = (row.get("departamento") or "").strip()
        prov_name = (row.get("provincia") or "").strip()
        dist_name = (row.get("distrito") or "").strip()

        if not ubigeo6 or len(ubigeo6) != 6:
            continue

        dep_code = ubigeo6[:2]
        prov_code = ubigeo6[:4]

        # Registrar departamento único
        if dep_code not in departamentos:
            departamentos[dep_code] = {
                "ubigeo": dep_code,
                "nombre": dep_name,
            }

        # Registrar provincia única
        if prov_code not in provincias:
            provincias[prov_code] = {
                "ubigeo": prov_code,
                "nombre": prov_name,
                "dep_code": dep_code,
            }

        # Registrar distrito (uno por fila)
        distritos.append(
            {
                "ubigeo": ubigeo6,
                "nombre": dist_name,
                "prov_code": prov_code,
            }
        )

    # 3) Crear Departamentos
    dep_objs = {}
    for dep_code, data in departamentos.items():
        dep, _ = Departamento.objects.update_or_create(
            ubigeo=data["ubigeo"],
            defaults={
                "nombre": data["nombre"],
            },
        )
        dep_objs[dep_code] = dep

    # 4) Crear Provincias
    prov_objs = {}
    for prov_code, data in provincias.items():
        dep_code = data["dep_code"]
        dep = dep_objs.get(dep_code)
        if not dep:
            raise ValueError(
                f"No se encontró Departamento con código {dep_code} "
                f"para la provincia {data['nombre']} ({prov_code})"
            )

        prov, _ = Provincia.objects.update_or_create(
            ubigeo=data["ubigeo"],
            defaults={
                "nombre": data["nombre"],
                "departamento": dep,
            },
        )
        prov_objs[prov_code] = prov

    # 5) Crear Distritos
    for dist in distritos:
        prov = prov_objs.get(dist["prov_code"])
        if not prov:
            raise ValueError(
                f"No se encontró Provincia con código {dist['prov_code']} "
                f"para el distrito {dist['nombre']} ({dist['ubigeo']})"
            )

        Distrito.objects.update_or_create(
            ubigeo=dist["ubigeo"],
            defaults={
                "nombre": dist["nombre"],
                "provincia": prov,
            },
        )


def unload_ubigeo_oficial(apps, schema_editor):
    """Reverse: borrar todo el catálogo de ubigeo (opcional)."""
    Departamento = apps.get_model("ubicaciones", "Departamento")
    Provincia = apps.get_model("ubicaciones", "Provincia")
    Distrito = apps.get_model("ubicaciones", "Distrito")

    Distrito.objects.all().delete()
    Provincia.objects.all().delete()
    Departamento.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        # 👇 IMPORTANTE: pon aquí la ÚLTIMA migración real de `ubicaciones`
        # por ejemplo, si tu última migración es 0003_auto_xxx:
        ("ubicaciones", "0003_load_ubigeo"),
        # Ajusta el nombre ("0003_load_ubigeo") según el archivo que tengas.
    ]

    operations = [
        migrations.RunPython(
            load_ubigeo_oficial,
            reverse_code=unload_ubigeo_oficial,
        ),
    ]