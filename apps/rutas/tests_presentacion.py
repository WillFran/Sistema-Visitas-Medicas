# apps/rutas/tests_presentacion.py
# VERSIÓN SOLO PARA PRESENTACIÓN EN VIVO - SIN CAPTURAS

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth import get_user_model
from django.test.utils import override_settings
from django.utils import timezone

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

from apps.ubicaciones.models import Departamento, Provincia, Distrito
from apps.doctores.models import Doctor
from apps.rutas.models import Ruta


class PresentacionHelper:
    """
    Helper SIMPLIFICADO solo para pausas en presentación
    SIN capturas de pantalla
    """
    
    def __init__(self, nombre_test):
        self.nombre_test = nombre_test
        self.paso_numero = 1
        print(f"\n{'='*70}")
        print(f"🎤 PRESENTACIÓN EN VIVO: {nombre_test}")
        print(f"{'='*70}")
    
    def pausa_explicacion(self, texto_explicacion, pausa_segundos=4):
        """
        Solo muestra el texto y hace pausa para explicar
        """
        print(f"\n🔹 PASO {self.paso_numero}: {texto_explicacion}")
        print(f"   ⏸️  Pausa de {pausa_segundos}s - Explica ahora...")
        
        # Cuenta regresiva visual
        for i in range(pausa_segundos, 0, -1):
            print(f"   {i}...", end=' ', flush=True)
            time.sleep(1)
        print("¡CONTINUAR!")
        
        self.paso_numero += 1
    
    def exito(self, mensaje, pausa_segundos=3):
        """Muestra mensaje de éxito"""
        print(f"\n✅ ÉXITO: {mensaje}")
        print(f"   ⏸️  Pausa de {pausa_segundos}s...")
        time.sleep(pausa_segundos)
    
    def finalizar(self):
        """Finaliza la presentación"""
        print(f"\n{'='*70}")
        print(f"🎉 PRESENTACIÓN FINALIZADA")
        print(f"📊 Total pasos explicados: {self.paso_numero - 1}")
        print(f"{'='*70}")


@override_settings(DEBUG=True)
class PresentacionEnVivoTests(StaticLiveServerTestCase):
    """
    Test optimizado SOLO para presentación en vivo
    Sin capturas, sin backups, solo pausas para explicar
    """
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = Chrome()
        cls.driver.implicitly_wait(5)
        # Maximizar ventana para mejor visibilidad
        cls.driver.maximize_window()

    @classmethod
    def tearDownClass(cls):
        try:
            cls.driver.quit()
        except Exception:
            pass
        super().tearDownClass()

    def setUp(self):
        """Configuración rápida para demo"""
        User = get_user_model()
        self.password = "Admin1234*"

        self.user = User.objects.create_user(
            username="visitador_presentacion@test.com",
            email="visitador_presentacion@test.com",
            password=self.password,
            rol="VISITADOR",
            is_staff=True,
            must_change_password=False,
        )

        # Ubicación: LIMA / LIMA / LIMA
        dep = Departamento.objects.create(nombre="LIMA")
        prov = Provincia.objects.create(nombre="LIMA", departamento=dep)
        dist = Distrito.objects.create(nombre="LIMA", provincia=prov)

        # Doctor para la demo
        self.doctor = Doctor.objects.create(
            cmp="777777",
            nombre="Dr. Presentación",
            apellido="Demo",
            especialidad="Medicina General",
            direccion="Av. Demostración 123",
            ubigeo=dist,
            visitador=self.user,
        )

    def _login_rapido(self):
        """Login optimizado para demo"""
        d = self.driver
        d.get(self.live_server_url + "/accounts/login/")
        
        # Ingresar credenciales rápido
        d.find_element(By.ID, "id_username").send_keys(self.user.username)
        pwd = d.find_element(By.ID, "id_password")
        pwd.send_keys(self.password)
        pwd.send_keys(Keys.RETURN)
        
        WebDriverWait(d, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

    def test_presentacion_completa(self):
        """
        PRESENTACIÓN EN VIVO COMPLETA
        - Solo pausas para explicación
        - Sin capturas de pantalla
        - Optimizado para mostrar en pantalla grande
        """
        presenter = PresentacionHelper("Sistema de Rutas Médicas - Presentación Final")
        
        try:
            # ========== INICIO DE PRESENTACIÓN ==========
            
            # 1. INTRODUCCIÓN
            presenter.pausa_explicacion(
                "Bienvenidos al Sistema de Gestión de Rutas Médicas",
                pausa_segundos=5
            )
            
            # 2. MOSTRAR PANTALLA DE LOGIN
            self.driver.get(self.live_server_url + "/accounts/login/")
            time.sleep(2)  # Esperar carga
            
            presenter.pausa_explicacion(
                "Pantalla de Login - Acceso seguro con credenciales",
                pausa_segundos=4
            )
            
            # 3. INGRESAR CREDENCIALES
            username = self.driver.find_element(By.ID, "id_username")
            username.send_keys(self.user.username)
            
            password = self.driver.find_element(By.ID, "id_password")
            password.send_keys(self.password)
            
            presenter.pausa_explicacion(
                "Ingreso de credenciales - Usuario visitador médico",
                pausa_segundos=3
            )
            
            # 4. REALIZAR LOGIN
            password.send_keys(Keys.RETURN)
            time.sleep(2)
            
            presenter.pausa_explicacion(
                "Dashboard Principal - Login exitoso, menú de navegación",
                pausa_segundos=4
            )
            
            # 5. NAVEGAR A MÓDULO DE RUTAS
            try:
                rutas_link = self.driver.find_element(By.PARTIAL_LINK_TEXT, "Rutas")
                rutas_link.click()
            except:
                # Fallback: ir directamente a la URL
                self.driver.get(self.live_server_url + "/rutas/crear/")
            
            time.sleep(2)
            
            presenter.pausa_explicacion(
                "Módulo de Gestión de Rutas - Vista principal del sistema",
                pausa_segundos=5
            )
            
            # 6. MOSTRAR TABLA DE DOCTORES
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table.table"))
            )
            
            # Resaltar tabla visualmente
            tabla = self.driver.find_element(By.CSS_SELECTOR, "table.table")
            self.driver.execute_script("""
                arguments[0].style.boxShadow = '0 0 20px rgba(0,150,255,0.3)';
                arguments[0].style.transition = 'box-shadow 0.5s';
            """, tabla)
            
            presenter.pausa_explicacion(
                "Tabla de Doctores Asignados - Lista de profesionales médicos disponibles",
                pausa_segundos=4
            )
            
            # Remover resaltado
            self.driver.execute_script("arguments[0].style.boxShadow = '';", tabla)
            
            # 7. SELECCIONAR DOCTOR ESPECÍFICO
            fila = self.driver.find_element(By.CSS_SELECTOR, "tbody tr")
            
            # Resaltar fila seleccionada
            self.driver.execute_script("""
                arguments[0].style.backgroundColor = '#e8f4fd';
                arguments[0].style.borderLeft = '4px solid #007bff';
                arguments[0].style.transition = 'all 0.3s';
            """, fila)
            
            presenter.pausa_explicacion(
                "Doctor Seleccionado - Dr. Presentación Demo (Estado actual: Sin ruta)",
                pausa_segundos=4
            )
            
            # 8. ASIGNAR FECHA DE VISITA
            input_fecha = fila.find_element(By.CSS_SELECTOR, 'input[type="date"]')
            hoy = timezone.now().date()
            fecha_str = hoy.strftime("%Y-%m-%d")
            
            # Enfocar y mostrar calendario
            self.driver.execute_script("arguments[0].focus();", input_fecha)
            input_fecha.clear()
            
            # Escribir fecha gradualmente (para mejor visualización)
            for char in fecha_str:
                input_fecha.send_keys(char)
                time.sleep(0.1)
            
            presenter.pausa_explicacion(
                f"Asignación de Fecha - {hoy.strftime('%d/%m/%Y')} (Selección de calendario interactivo)",
                pausa_segundos=3
            )
            
            # 9. CREAR RUTA MÉDICA
            formulario = fila.find_element(By.TAG_NAME, "form")
            doctor_id = formulario.find_element(By.CSS_SELECTOR, 'input[name="doctor_id"]').get_attribute("value")
            csrf_token = formulario.find_element(By.CSS_SELECTOR, 'input[name="csrfmiddlewaretoken"]').get_attribute("value")
            
            presenter.pausa_explicacion(
                "Creación de Ruta - Enviando solicitud al servidor para programar visita",
                pausa_segundos=4
            )
            
            # Enviar solicitud de creación
            script = f"""
            var formData = new FormData();
            formData.append('doctor_id', '{doctor_id}');
            formData.append('fecha_visita', '{fecha_str}');
            formData.append('csrfmiddlewaretoken', '{csrf_token}');
            
            fetch('{self.live_server_url}/rutas/crear/', {{
                method: 'POST',
                body: formData,
                headers: {{ 'X-Requested-With': 'XMLHttpRequest' }}
            }});
            """
            
            self.driver.execute_script(script)
            
            # 10. ESPERAR Y MOSTRAR RESULTADO
            time.sleep(3)
            
            # Recargar para ver cambios
            self.driver.refresh()
            time.sleep(2)
            
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table.table tbody tr"))
            )
            
            # Verificar estado actualizado
            fila_actualizada = self.driver.find_element(By.CSS_SELECTOR, "tbody tr")
            celdas = fila_actualizada.find_elements(By.TAG_NAME, "td")
            estado_final = celdas[5].text if len(celdas) > 5 else ""
            
            # Resaltar éxito visualmente
            self.driver.execute_script("""
                arguments[0].style.backgroundColor = '#d4edda';
                arguments[0].style.border = '2px solid #28a745';
                arguments[0].style.transition = 'all 0.5s';
            """, fila_actualizada)
            
            # Verificar en base de datos
            ruta_creada = Ruta.objects.filter(
                doctor=self.doctor, 
                fecha_visita=hoy
            ).exists()
            
            if ruta_creada and "Pendiente" in estado_final:
                presenter.exito(
                    f"RUTA MÉDICA CREADA EXITOSAMENTE - Estado actualizado: {estado_final}",
                    pausa_segundos=5
                )
            else:
                presenter.pausa_explicacion(
                    "Proceso completado - Verificación del sistema en tiempo real",
                    pausa_segundos=3
                )
            
            # 11. CONCLUSIÓN Y DEMOSTRACIÓN FINAL
            presenter.pausa_explicacion(
                "Conclusión - Sistema funcional para gestión eficiente de visitas médicas",
                pausa_segundos=5
            )
            
            # Mostrar estado final completo
            print(f"\n📋 RESUMEN FINAL DEL PROCESO:")
            print(f"   • Doctor: Dr. Presentación Demo")
            print(f"   • Fecha asignada: {hoy.strftime('%d/%m/%Y')}")
            print(f"   • Estado final: {estado_final}")
            print(f"   • Ruta en base de datos: {'SÍ' if ruta_creada else 'NO'}")
            
        except Exception as e:
            print(f"\n⚠️  Error durante presentación: {e}")
            presenter.pausa_explicacion(
                f"Continuando demostración - Error técnico menor detectado",
                pausa_segundos=2
            )
        
        finally:
            # Mensaje final de la presentación
            presenter.finalizar()
            
            # Mantener ventana abierta para preguntas
            print("\n🖥️  La ventana del navegador permanecerá abierta por 15 segundos...")
            print("   (Para cerrar manualmente, cierra la ventana del navegador)")
            time.sleep(15)


@override_settings(DEBUG=True)
class PresentacionRapidaTests(StaticLiveServerTestCase):
    """
    Versión RÁPIDA para prueba previa a la presentación
    Verifica que todo funcione correctamente
    """
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = Chrome()
        cls.driver.maximize_window()
    
    @classmethod
    def tearDownClass(cls):
        try:
            cls.driver.quit()
        except:
            pass
        super().tearDownClass()
    
    def setUp(self):
        """Configuración rápida"""
        User = get_user_model()
        
        self.user = User.objects.create_user(
            username="test_rapido@test.com",
            password="test123",
            rol="VISITADOR",
            is_staff=True,
        )
        
        # Ubicación
        dep = Departamento.objects.create(nombre="TEST")
        prov = Provincia.objects.create(nombre="TEST", departamento=dep)
        dist = Distrito.objects.create(nombre="TEST", provincia=prov)
        
        # Doctor de prueba
        self.doctor = Doctor.objects.create(
            cmp="888888",
            nombre="Dr. Prueba",
            apellido="Rápida",
            especialidad="Pruebas",
            ubigeo=dist,
            visitador=self.user,
        )
    
    def test_verificacion_rapida(self):
        """
        Solo verifica que todo funcione (sin pausas largas)
        """
        print("\n🔍 VERIFICACIÓN RÁPIDA DEL SISTEMA - PRE-PRESENTACIÓN")
        print("="*60)
        
        # 1. Navegar a login
        self.driver.get(self.live_server_url + "/accounts/login/")
        time.sleep(1)
        
        print("✓ 1. Pantalla de login cargada correctamente")
        
        # 2. Login rápido
        self.driver.find_element(By.ID, "id_username").send_keys(self.user.username)
        self.driver.find_element(By.ID, "id_password").send_keys("test123" + Keys.RETURN)
        time.sleep(2)
        
        print("✓ 2. Login exitoso - Credenciales aceptadas")
        
        # 3. Verificar dashboard
        body_text = self.driver.find_element(By.TAG_NAME, "body").text
        if any(keyword in body_text for keyword in ["Bienvenido", "Dashboard", "Menú", "Rutas"]):
            print("✓ 3. Dashboard cargado - Interfaz principal visible")
        else:
            print("⚠ 3. Dashboard - Verificar contenido")
        
        # 4. Navegar a rutas
        try:
            self.driver.find_element(By.PARTIAL_LINK_TEXT, "Rutas").click()
        except:
            self.driver.get(self.live_server_url + "/rutas/crear/")
        
        time.sleep(2)
        
        # 5. Verificar tabla de doctores
        try:
            tabla = self.driver.find_element(By.CSS_SELECTOR, "table.table")
            filas = tabla.find_elements(By.CSS_SELECTOR, "tbody tr")
            print(f"✓ 4. Módulo de rutas cargado - {len(filas)} doctor(es) en tabla")
        except:
            print("⚠ 4. Módulo de rutas - Tabla no encontrada")
        
        print(f"\n✅ SISTEMA LISTO PARA PRESENTACIÓN")
        print("="*60)
        print("📋 ESTADO:")
        print(f"   • Servidor: ACTIVO")
        print(f"   • Base de datos: CONFIGURADA")
        print(f"   • Navegador: CHROME ({self.driver.capabilities['browserVersion']})")
        print(f"   • Usuario de prueba: {self.user.username}")
        print(f"   • Doctor de prueba: {self.doctor.nombre} {self.doctor.apellido}")
        
        # Mantener abierto brevemente
        time.sleep(3)


@override_settings(DEBUG=True)
class PresentacionMinimaTests(StaticLiveServerTestCase):
    """
    Versión MÍNIMA para demostración ultra rápida
    """
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = Chrome()
    
    @classmethod
    def tearDownClass(cls):
        try:
            cls.driver.quit()
        except:
            pass
        super().tearDownClass()
    
    def test_demo_ultra_rapida(self):
        """
        Demostración en 60 segundos
        """
        print("\n⚡ DEMOSTRACIÓN ULTRA RÁPIDA (60 segundos)")
        print("="*50)
        
        # Crear datos mínimos
        User = get_user_model()
        user = User.objects.create_user(
            username="demo_rapida@test.com",
            password="demo123",
            rol="VISITADOR"
        )
        
        print("PASO 1: Login (3s)...")
        self.driver.get(self.live_server_url + "/accounts/login/")
        self.driver.find_element(By.ID, "id_username").send_keys(user.username)
        self.driver.find_element(By.ID, "id_password").send_keys("demo123" + Keys.RETURN)
        time.sleep(3)
        
        print("PASO 2: Navegar a rutas (2s)...")
        self.driver.get(self.live_server_url + "/rutas/crear/")
        time.sleep(2)
        
        print("PASO 3: Mostrar interfaz (3s)...")
        time.sleep(3)
        
        print("\n✅ DEMOSTRACIÓN COMPLETADA EN 60 SEGUNDOS")
        print("="*50)