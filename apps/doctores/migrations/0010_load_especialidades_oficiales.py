from django.db import migrations


def cargar_especialidades(apps, schema_editor):
    Especialidad = apps.get_model("doctores", "Especialidad")

    especialidades = [
        ("Medicina General", "MED-GEN"),
        ("Medicina Familiar y Comunitaria", "MED-FAM"),
        ("Medicina Interna", "MED-INT"),
        ("Cardiología", "CARD"),
        ("Neumología", "NEUM"),
        ("Gastroenterología", "GAST"),
        ("Nefrología", "NEFR"),
        ("Endocrinología", "ENDO"),
        ("Reumatología", "REUM"),
        ("Hematología", "HEMA"),
        ("Oncología Médica", "ONC-MED"),
        ("Infectología", "INFEC"),
        ("Pediatría", "PED"),
        ("Neonatología", "NEO"),
        ("Ginecología y Obstetricia", "GIN-OBS"),
        ("Medicina Materno Fetal", "MAT-FET"),
        ("Cirugía General", "CIR-GEN"),
        ("Traumatología y Ortopedia", "TRAUMA"),
        ("Neurocirugía", "NEUROC"),
        ("Cirugía Plástica y Reconstructiva", "CIR-PLAS"),
        ("Cirugía Cardiovascular", "CIR-CV"),
        ("Neurología", "NEURO"),
        ("Psiquiatría", "PSIQ"),
        ("Dermatología", "DERM"),
        ("Oftalmología", "OFT"),
        ("Otorrinolaringología", "OTOR"),
        ("Urología", "UROL"),
        ("Anestesiología", "ANES"),
        ("Medicina de Emergencias y Desastres", "EMERG"),
        ("Radiología", "RADIO"),
        ("Medicina Física y Rehabilitación", "REHAB"),
        ("Medicina Ocupacional y del Medio Ambiente", "MED-OCC"),
    ]

    for nombre, codigo in especialidades:
        Especialidad.objects.get_or_create(
            nombre=nombre,
            defaults={"codigo_cmp": codigo}
        )


def revertir_especialidades(apps, schema_editor):
    Especialidad = apps.get_model("doctores", "Especialidad")
    nombres = [
        "Medicina General",
        "Medicina Familiar y Comunitaria",
        "Medicina Interna",
        "Cardiología",
        "Neumología",
        "Gastroenterología",
        "Nefrología",
        "Endocrinología",
        "Reumatología",
        "Hematología",
        "Oncología Médica",
        "Infectología",
        "Pediatría",
        "Neonatología",
        "Ginecología y Obstetricia",
        "Medicina Materno Fetal",
        "Cirugía General",
        "Traumatología y Ortopedia",
        "Neurocirugía",
        "Cirugía Plástica y Reconstructiva",
        "Cirugía Cardiovascular",
        "Neurología",
        "Psiquiatría",
        "Dermatología",
        "Oftalmología",
        "Otorrinolaringología",
        "Urología",
        "Anestesiología",
        "Medicina de Emergencias y Desastres",
        "Radiología",
        "Medicina Física y Rehabilitación",
        "Medicina Ocupacional y del Medio Ambiente",
    ]
    Especialidad.objects.filter(nombre__in=nombres).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("doctores", "0009_especialidad_alter_doctor_options_and_more"),
    ]

    operations = [
        migrations.RunPython(
            cargar_especialidades,
            reverse_code=revertir_especialidades,
        ),
    ]