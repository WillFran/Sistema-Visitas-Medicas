# tests_demo.py - VERSIÓN PARA DEMO EN VIVO + BACKUP AUTOMÁTICO

import time
import os
from datetime import datetime

class DemoHelper:
    """
    Helper ULTRA simple para:
    1. Pausas en vivo durante la explicación
    2. Capturas automáticas como backup
    3. Cero complicaciones
    """
    
    def __init__(self, driver, nombre_test):
        self.driver = driver
        self.nombre_test = nombre_test
        self.paso_numero = 1
        
        # Crear carpeta simple para capturas
        self.carpeta_capturas = f"capturas_demo_{datetime.now().strftime('%Y%m%d')}"
        if not os.path.exists(self.carpeta_capturas):
            os.makedirs(self.carpeta_capturas)
        
        # Archivo de notas para tu guión
        self.notas_file = open(f"{self.carpeta_capturas}/guion_explicacion.txt", "w")
        self.notas_file.write(f"Guion para demo: {nombre_test}\n")
        self.notas_file.write(f"Fecha: {datetime.now()}\n\n")
    
    def mostrar_paso(self, texto_explicacion, pausa_segundos=4, capturar=True):
        """
        Método ÚNICO que necesitas
        """
        print(f"\n{'='*50}")
        print(f"PASO {self.paso_numero}: {texto_explicacion}")
        print(f"{'='*50}")
        
        # 1. Escribir en guión (para tu referencia)
        self.notas_file.write(f"\nPASO {self.paso_numero}: {texto_explicacion}\n")
        
        # 2. Tomar captura SIEMPRE (backup automático)
        if capturar:
            nombre_archivo = f"paso_{self.paso_numero:02d}_{texto_explicacion[:20].replace(' ', '_')}.png"
            ruta_completa = f"{self.carpeta_capturas}/{nombre_archivo}"
            
            try:
                self.driver.save_screenshot(ruta_completa)
                print(f"📸 Captura automática: {nombre_archivo}")
                self.notas_file.write(f"   Captura: {nombre_archivo}\n")
            except:
                print("⚠️  No se pudo tomar captura (pantalla no disponible)")
        
        # 3. Pausa para explicar EN VIVO
        print(f"⏸️  Pausa de {pausa_segundos}s - Explica este paso ahora...")
        
        # Mostrar cuenta regresiva
        for i in range(pausa_segundos, 0, -1):
            print(f"   {i}...", end=' ', flush=True)
            time.sleep(1)
        print("¡SIGUIENTE!")
        
        self.paso_numero += 1
    
    def finalizar_demo(self):
        """Cierra todo limpiamente"""
        self.notas_file.write(f"\n\n--- FIN DE DEMO ---\n")
        self.notas_file.write(f"Total pasos: {self.paso_numero - 1}\n")
        self.notas_file.close()
        
        print(f"\n{'='*50}")
        print(f"✅ DEMO COMPLETADA")
        print(f"📁 Capturas guardadas en: {self.carpeta_capturas}/")
        print(f"📝 Guión en: {self.carpeta_capturas}/guion_explicacion.txt")
        print(f"{'='*50}")
        
        # Mostrar resumen rápido
        if os.path.exists(self.carpeta_capturas):
            capturas = [f for f in os.listdir(self.carpeta_capturas) if f.endswith('.png')]
            print(f"📸 Total capturas: {len(capturas)}")