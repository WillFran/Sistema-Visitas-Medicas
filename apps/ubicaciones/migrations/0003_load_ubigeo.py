from django.db import migrations


def load_ubigeo(apps, schema_editor):
    Departamento = apps.get_model("ubicaciones", "Departamento")
    Provincia = apps.get_model("ubicaciones", "Provincia")
    Distrito = apps.get_model("ubicaciones", "Distrito")

    # ==========================================================
    # 1) CARGAR DEPARTAMENTOS (UBIGEO OFICIAL INEI)
    # ==========================================================

    departamentos_data = [
        {"ubigeo": "01", "nombre": "Amazonas"},
        {"ubigeo": "02", "nombre": "Áncash"},
        {"ubigeo": "03", "nombre": "Apurímac"},
        {"ubigeo": "04", "nombre": "Arequipa"},
        {"ubigeo": "05", "nombre": "Ayacucho"},
        {"ubigeo": "06", "nombre": "Cajamarca"},
        {"ubigeo": "07", "nombre": "Callao"},
        {"ubigeo": "08", "nombre": "Cusco"},
        {"ubigeo": "09", "nombre": "Huancavelica"},
        {"ubigeo": "10", "nombre": "Huánuco"},
        {"ubigeo": "11", "nombre": "Ica"},
        {"ubigeo": "12", "nombre": "Junín"},
        {"ubigeo": "13", "nombre": "La Libertad"},
        {"ubigeo": "14", "nombre": "Lambayeque"},
        {"ubigeo": "15", "nombre": "Lima"},
        {"ubigeo": "16", "nombre": "Loreto"},
        {"ubigeo": "17", "nombre": "Madre de Dios"},
        {"ubigeo": "18", "nombre": "Moquegua"},
        {"ubigeo": "19", "nombre": "Pasco"},
        {"ubigeo": "20", "nombre": "Piura"},
        {"ubigeo": "21", "nombre": "Puno"},
        {"ubigeo": "22", "nombre": "San Martín"},
        {"ubigeo": "23", "nombre": "Tacna"},
        {"ubigeo": "24", "nombre": "Tumbes"},
        {"ubigeo": "25", "nombre": "Ucayali"},
    ]

    for dep in departamentos_data:
        # No borramos nada, solo actualizamos o creamos.
        Departamento.objects.update_or_create(
            nombre=dep["nombre"],
            defaults={"ubigeo": dep["ubigeo"]},
        )

    # ==========================================================
    # 2) CARGAR PROVINCIAS (EJEMPLO DE ESTRUCTURA)
    # ==========================================================
    # Aquí te pongo la ESTRUCTURA para provincias con algunos ejemplos.
    # La idea es que luego completes la lista con TODAS las provincias.
    #
    # ubigeo_provincia: 4 dígitos
    # - 2 primeros: departamento
    # - 2 siguientes: código de provincia dentro del departamento

    provincias_data = [
        # Amazonas (01)
        {"ubigeo": "0101", "nombre": "Chachapoyas", "dep_ubigeo": "01"},
        {"ubigeo": "0102", "nombre": "Bagua", "dep_ubigeo": "01"},

        # Lima (15)
        {"ubigeo": "1501", "nombre": "Lima", "dep_ubigeo": "15"},
        {"ubigeo": "1502", "nombre": "Barranca", "dep_ubigeo": "15"},
        {"ubigeo": "1503", "nombre": "Cajatambo", "dep_ubigeo": "15"},

        # San Martín (22)
        {"ubigeo": "2201", "nombre": "Moyobamba", "dep_ubigeo": "22"},
        {"ubigeo": "2202", "nombre": "Bellavista", "dep_ubigeo": "22"},
        {"ubigeo": "2203", "nombre": "El Dorado", "dep_ubigeo": "22"},
        {"ubigeo": "2204", "nombre": "Huallaga", "dep_ubigeo": "22"},
        {"ubigeo": "2205", "nombre": "Lamas", "dep_ubigeo": "22"},
        {"ubigeo": "2206", "nombre": "Mariscal Cáceres", "dep_ubigeo": "22"},
        {"ubigeo": "2207", "nombre": "Picota", "dep_ubigeo": "22"},
        {"ubigeo": "2208", "nombre": "Rioja", "dep_ubigeo": "22"},
        {"ubigeo": "2209", "nombre": "San Martín", "dep_ubigeo": "22"},
        {"ubigeo": "2210", "nombre": "Tocache", "dep_ubigeo": "22"},

        # ... aquí agregas TODAS las provincias restantes
    ]

    for prov in provincias_data:
        dep = Departamento.objects.get(ubigeo=prov["dep_ubigeo"])
        Provincia.objects.update_or_create(
            nombre=prov["nombre"],
            departamento=dep,
            defaults={"ubigeo": prov["ubigeo"]},
        )

    # ==========================================================
    # 3) CARGAR DISTRITOS (EJEMPLO DE ESTRUCTURA)
    # ==========================================================
    # Igual idea para distritos:
    # - ubigeo 6 dígitos: 2 dep + 2 prov + 2 distrito

    distritos_data = [
        # Algunos ejemplos reales para que tengas el formato:
        # Provincia: Chachapoyas (0101)
        {"ubigeo": "010101", "nombre": "Chachapoyas", "prov_ubigeo": "0101"},
        {"ubigeo": "010102", "nombre": "Asunción", "prov_ubigeo": "0101"},
        {"ubigeo": "010103", "nombre": "Balsas", "prov_ubigeo": "0101"},

        # Provincia: Lima (1501)
        {"ubigeo": "150101", "nombre": "Lima", "prov_ubigeo": "1501"},
        {"ubigeo": "150102", "nombre": "Ancón", "prov_ubigeo": "1501"},
        {"ubigeo": "150103", "nombre": "Ate", "prov_ubigeo": "1501"},
        {"ubigeo": "150104", "nombre": "Barranco", "prov_ubigeo": "1501"},
        {"ubigeo": "150105", "nombre": "Breña", "prov_ubigeo": "1501"},

        # Provincia: San Martín (2209)
        {"ubigeo": "220901", "nombre": "Tarapoto", "prov_ubigeo": "2209"},
        {"ubigeo": "220902", "nombre": "Alberto Leveau", "prov_ubigeo": "2209"},
        {"ubigeo": "220903", "nombre": "Cacatachi", "prov_ubigeo": "2209"},
        {"ubigeo": "220904", "nombre": "Chazuta", "prov_ubigeo": "2209"},
        {"ubigeo": "220905", "nombre": "Chipurana", "prov_ubigeo": "2209"},
        {"ubigeo": "220906", "nombre": "El Porvenir", "prov_ubigeo": "2209"},
        {"ubigeo": "220907", "nombre": "Huimbayoc", "prov_ubigeo": "2209"},
        {"ubigeo": "220908", "nombre": "Juan Guerra", "prov_ubigeo": "2209"},
        {"ubigeo": "220909", "nombre": "La Banda de Shilcayo", "prov_ubigeo": "2209"},
        {"ubigeo": "220910", "nombre": "Morales", "prov_ubigeo": "2209"},
        {"ubigeo": "220911", "nombre": "Papaplaya", "prov_ubigeo": "2209"},
        {"ubigeo": "220912", "nombre": "San Antonio", "prov_ubigeo": "2209"},
        {"ubigeo": "220913", "nombre": "Sauce", "prov_ubigeo": "2209"},
        {"ubigeo": "220914", "nombre": "Shapaja", "prov_ubigeo": "2209"},

        # ... aquí completarías todos los distritos restantes
    ]

    for dist in distritos_data:
        prov = Provincia.objects.get(ubigeo=dist["prov_ubigeo"])
        Distrito.objects.update_or_create(
            nombre=dist["nombre"],
            provincia=prov,
            defaults={"ubigeo": dist["ubigeo"]},
        )


def unload_ubigeo(apps, schema_editor):
    """
    Backwards simple: opcional.
    En un sistema del Estado normalmente NO se borran estas tablas,
    pero lo dejamos por completitud.
    """
    Departamento = apps.get_model("ubicaciones", "Departamento")
    Provincia = apps.get_model("ubicaciones", "Provincia")
    Distrito = apps.get_model("ubicaciones", "Distrito")

    # Si quieres que el reverse no borre nada, deja este cuerpo vacío (pass)
    # Aquí lo dejo eliminando datos por simplicidad, pero puedes cambiarlo.
    Distrito.objects.all().delete()
    Provincia.objects.all().delete()
    Departamento.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("ubicaciones", "0002_alter_departamento_options_alter_distrito_options_and_more"),
    ]

    operations = [
        migrations.RunPython(load_ubigeo, reverse_code=unload_ubigeo),
    ]