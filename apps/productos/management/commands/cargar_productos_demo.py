from django.core.management.base import BaseCommand
from apps.productos.models import Producto


class Command(BaseCommand):
    help = "Carga un set de productos demo en la tabla Producto."

    def handle(self, *args, **options):
        productos_demo = [
            # ================= RX / Marca =================
            {
                "codigo_interno": "NAYF400TAB",
                "nombre": "Nayflex 400 mg",
                "dci": "Ibuprofeno",
                "forma_farmaceutica": "Tableta recubierta",
                "concentracion": "400 mg",
                "presentacion": "Caja x 10 blíster x 10 tabletas",
                "categoria": "Analgésico / Antiinflamatorio (AINE)",
                "codigo_atc": "M01AE01",
                "gtin": "",
                "tipo_producto": "prescribible",
            },
            {
                "codigo_interno": "IBUC400SUSP",
                "nombre": "Ibucalm Suspensión",
                "dci": "Ibuprofeno",
                "forma_farmaceutica": "Suspensión oral",
                "concentracion": "100 mg/5 mL",
                "presentacion": "Frasco x 150 mL",
                "categoria": "Analgésico / Antipirético pediátrico",
                "codigo_atc": "M01AE01",
                "gtin": "",
                "tipo_producto": "prescribible",
            },
            {
                "codigo_interno": "GRIPMAXCAP",
                "nombre": "Gripamax Cápsulas",
                "dci": "Paracetamol + Fenilefrina + Cafeína",
                "forma_farmaceutica": "Cápsula",
                "concentracion": "500 mg + 5 mg + 30 mg",
                "presentacion": "Caja x 10 blíster x 10 cápsulas",
                "categoria": "Antigripal / Analgésico",
                "codigo_atc": "",
                "gtin": "",
                "tipo_producto": "prescribible",
            },
            {
                "codigo_interno": "PROSTACAPS",
                "nombre": "Prostamicil Cápsulas",
                "dci": "Extracto de Serenoa repens",
                "forma_farmaceutica": "Cápsula blanda",
                "concentracion": "320 mg",
                "presentacion": "Caja x 3 blíster x 10 cápsulas",
                "categoria": "Urología / Hiperplasia prostática benigna",
                "codigo_atc": "",
                "gtin": "",
                "tipo_producto": "prescribible",
            },

            # ================= Muestras médicas =================
            {
                "codigo_interno": "NAYF400MUE",
                "nombre": "Nayflex 400 mg – Muestra",
                "dci": "Ibuprofeno",
                "forma_farmaceutica": "Tableta recubierta",
                "concentracion": "400 mg",
                "presentacion": "Sobre x 2 tabletas (muestra médica)",
                "categoria": "Analgésico / Antiinflamatorio (AINE)",
                "codigo_atc": "M01AE01",
                "gtin": "",
                "tipo_producto": "muestra",
            },
            {
                "codigo_interno": "IBUC400MUE",
                "nombre": "Ibucalm Suspensión – Muestra",
                "dci": "Ibuprofeno",
                "forma_farmaceutica": "Suspensión oral",
                "concentracion": "100 mg/5 mL",
                "presentacion": "Frasco x 30 mL (muestra médica)",
                "categoria": "Analgésico / Antipirético pediátrico",
                "codigo_atc": "M01AE01",
                "gtin": "",
                "tipo_producto": "muestra",
            },

            # ================= Material promocional =================
            {
                "codigo_interno": "MATNAYFTRIP",
                "nombre": "Tríptico Nayflex",
                "dci": "",
                "forma_farmaceutica": "",
                "concentracion": "",
                "presentacion": "Tríptico informativo para médicos",
                "categoria": "Material promocional impreso",
                "codigo_atc": "",
                "gtin": "",
                "tipo_producto": "promocional",
            },
            {
                "codigo_interno": "MATIBUPOS",
                "nombre": "Afiche Ibucalm pediátrico",
                "dci": "",
                "forma_farmaceutica": "",
                "concentracion": "",
                "presentacion": "Póster tamaño A3 para consultorio",
                "categoria": "Material promocional impreso",
                "codigo_atc": "",
                "gtin": "",
                "tipo_producto": "promocional",
            },

            # ================= Merchandising =================
            {
                "codigo_interno": "MERCHLAPNAY",
                "nombre": "Lapicero Nayflex",
                "dci": "",
                "forma_farmaceutica": "",
                "concentracion": "",
                "presentacion": "Lapicero institucional con logo Nayflex",
                "categoria": "Merchandising",
                "codigo_atc": "",
                "gtin": "",
                "tipo_producto": "merch",
            },
            {
                "codigo_interno": "MERCHBLOCKIBU",
                "nombre": "Block de notas Ibucalm",
                "dci": "",
                "forma_farmaceutica": "",
                "concentracion": "",
                "presentacion": "Block de notas tamaño A6 con logo Ibucalm",
                "categoria": "Merchandising",
                "codigo_atc": "",
                "gtin": "",
                "tipo_producto": "merch",
            },
        ]

        creados = 0
        actualizados = 0

        for data in productos_demo:
            obj, created = Producto.objects.update_or_create(
                codigo_interno=data["codigo_interno"],
                defaults=data,
            )
            if created:
                creados += 1
            else:
                actualizados += 1

        self.stdout.write(self.style.SUCCESS(
            f"Productos demo cargados. Nuevos: {creados}, Actualizados: {actualizados}"
        ))
