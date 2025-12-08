# apps/rutas/test_diagnostico_formulario.py

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth import get_user_model
from django.test import override_settings
from django.utils import timezone

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import time

from apps.ubicaciones.models import Departamento, Provincia, Distrito
from apps.doctores.models import Doctor


@override_settings(DEBUG=True)
class DiagnosticoFormularioTest(StaticLiveServerTestCase):
    """Diagnóstico del formulario de creación de rutas"""
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        
        options = ChromeOptions()
        options.add_argument('--window-size=1920,1080')
        
        cls.driver = Chrome(options=options)
        cls.driver.implicitly_wait(10)
    
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()
    
    def setUp(self):
        User = get_user_model()
        self.password = "Test1234*"
        
        self.user = User.objects.create_user(
            username="diagnostico@test.com",
            password=self.password,
            rol="VISITADOR",
            is_staff=True,
        )
        
        dep = Departamento.objects.create(nombre="DIAG")
        prov = Provincia.objects.create(nombre="DIAG", departamento=dep)
        dist = Distrito.objects.create(nombre="DIAG", provincia=prov)
        
        self.doctor = Doctor.objects.create(
            cmp="DIAG123",
            nombre="Doctor Diagnóstico",
            apellido="Test",
            especialidad="M.G.",
            direccion="Calle Diagnóstico 123",
            ubigeo=dist,
            visitador=self.user,
        )
    
    def test_diagnostico_detallado_formulario(self):
        """Diagnóstico DETALLADO del formulario"""
        print("\n" + "="*80)
        print("DIAGNÓSTICO DETALLADO DEL FORMULARIO")
        print("="*80)
        
        d = self.driver
        
        # 1. Login
        d.get(self.live_server_url + "/accounts/login/")
        time.sleep(2)
        
        d.find_element(By.ID, "id_username").send_keys(self.user.username)
        d.find_element(By.ID, "id_password").send_keys(self.password + Keys.RETURN)
        time.sleep(3)
        
        # 2. Ir a rutas
        d.get(self.live_server_url + "/rutas/crear/")
        time.sleep(3)
        
        # 3. ANALIZAR FORMULARIO
        print("\n1. ANALIZANDO FORMULARIO...")
        
        # Encontrar tabla y formulario
        tabla = d.find_element(By.CSS_SELECTOR, "table.table")
        fila = tabla.find_element(By.CSS_SELECTOR, "tbody tr")
        formulario = fila.find_element(By.TAG_NAME, "form")
        
        # Análisis del formulario
        print(f"\n   Atributos del formulario:")
        print(f"   - action: '{formulario.get_attribute('action')}'")
        print(f"   - method: '{formulario.get_attribute('method')}'")
        print(f"   - onsubmit: '{formulario.get_attribute('onsubmit')}'")
        print(f"   - id: '{formulario.get_attribute('id')}'")
        print(f"   - class: '{formulario.get_attribute('class')}'")
        
        # Analizar todos los inputs
        print(f"\n   Inputs del formulario:")
        inputs = formulario.find_elements(By.TAG_NAME, "input")
        for i, inp in enumerate(inputs):
            tipo = inp.get_attribute("type") or "text"
            nombre = inp.get_attribute("name") or "[sin nombre]"
            valor = inp.get_attribute("value") or "[vacío]"
            print(f"   [{i+1}] type='{tipo}', name='{nombre}', value='{valor}'")
        
        # Analizar botón
        print(f"\n   Botón del formulario:")
        boton = formulario.find_element(By.CSS_SELECTOR, "button")
        print(f"   - type: '{boton.get_attribute('type')}'")
        print(f"   - texto: '{boton.text}'")
        print(f"   - onclick: '{boton.get_attribute('onclick')}'")
        
        # 4. VERIFICAR JAVASCRIPT
        print("\n2. VERIFICANDO JAVASCRIPT...")
        
        # Verificar si hay event listeners
        script_listeners = """
        var form = arguments[0];
        var listeners = [];
        
        // Obtener event listeners (solo Chrome)
        if (window.getEventListeners) {
            var formListeners = window.getEventListeners(form);
            for (var eventType in formListeners) {
                formListeners[eventType].forEach(function(listener) {
                    listeners.push({
                        event: eventType,
                        listener: listener.listener.toString().substring(0, 100) + "..."
                    });
                });
            }
        }
        
        // Verificar botón también
        var button = form.querySelector('button[type="submit"]');
        var buttonListeners = [];
        if (button && window.getEventListeners) {
            var btnListeners = window.getEventListeners(button);
            for (var eventType in btnListeners) {
                btnListeners[eventType].forEach(function(listener) {
                    buttonListeners.push({
                        event: eventType,
                        listener: listener.listener.toString().substring(0, 100) + "..."
                    });
                });
            }
        }
        
        return {
            formListeners: listeners,
            buttonListeners: buttonListeners
        };
        """
        
        try:
            listeners = d.execute_script(script_listeners, formulario)
            print(f"   Event listeners del formulario: {len(listeners['formListeners'])}")
            for listener in listeners['formListeners']:
                print(f"     - {listener['event']}: {listener['listener']}")
            
            print(f"   Event listeners del botón: {len(listeners['buttonListeners'])}")
            for listener in listeners['buttonListeners']:
                print(f"     - {listener['event']}: {listener['listener']}")
        except:
            print("   ⚠️  No se pudieron obtener event listeners")
        
        # 5. PROBAR SUBMIT MANUAL
        print("\n3. PROBANDO SUBMIT MANUAL...")
        
        # Llenar fecha
        input_fecha = formulario.find_element(By.CSS_SELECTOR, "input[type='date']")
        hoy = timezone.now().date().strftime("%Y-%m-%d")
        
        # Limpiar y llenar
        d.execute_script("arguments[0].value = '';", input_fecha)
        input_fecha.send_keys(hoy)
        print(f"   Fecha ingresada: {hoy}")
        
        # Screenshot antes
        d.save_screenshot("diagnostico_antes_submit.png")
        
        # Intentar submit de varias formas
        print("\n   Probando diferentes métodos de submit:")
        
        # Método 1: Click normal en botón
        print("   a) Click normal en botón...")
        boton.click()
        time.sleep(2)
        url_despues_click = d.current_url
        print(f"      URL después de click: {url_despues_click}")
        
        # Volver atrás si cambió
        if d.current_url != self.live_server_url + "/rutas/crear/":
            d.back()
            time.sleep(2)
            # Re-encontrar elementos
            tabla = d.find_element(By.CSS_SELECTOR, "table.table")
            fila = tabla.find_element(By.CSS_SELECTOR, "tbody tr")
            formulario = fila.find_element(By.TAG_NAME, "form")
        
        # Método 2: Submit vía JavaScript
        print("   b) Submit vía JavaScript...")
        d.execute_script("arguments[0].submit();", formulario)
        time.sleep(2)
        url_despues_js = d.current_url
        print(f"      URL después de JS submit: {url_despues_js}")
        
        if d.current_url != self.live_server_url + "/rutas/crear/":
            d.back()
            time.sleep(2)
        
        # Método 3: Disparar evento submit
        print("   c) Disparar evento submit...")
        script_submit_event = """
        var form = arguments[0];
        var event = new Event('submit', {
            bubbles: true,
            cancelable: true
        });
        
        var wasCancelled = !form.dispatchEvent(event);
        return {
            eventDispatched: true,
            wasCancelled: wasCancelled
        };
        """
        
        resultado_evento = d.execute_script(script_submit_event, formulario)
        print(f"      Evento disparado: {resultado_evento['eventDispatched']}")
        print(f"      Fue cancelado: {resultado_evento['wasCancelled']}")
        time.sleep(2)
        
        # 6. VERIFICAR SI EL FORMULARIO ENVÍA DATOS
        print("\n4. VERIFICANDO ENVÍO DE DATOS...")
        
        # Interceptar fetch/XMLHttpRequest
        script_intercept = """
        // Interceptar todas las peticiones
        window.interceptedRequests = [];
        
        var originalFetch = window.fetch;
        window.fetch = function() {
            console.log("Fetch interceptado:", arguments);
            window.interceptedRequests.push({
                type: 'fetch',
                url: arguments[0],
                method: arguments[1] ? arguments[1].method : 'GET',
                timestamp: new Date().toISOString()
            });
            return originalFetch.apply(this, arguments);
        };
        
        var originalXHROpen = XMLHttpRequest.prototype.open;
        XMLHttpRequest.prototype.open = function() {
            console.log("XHR interceptado:", arguments);
            window.interceptedRequests.push({
                type: 'xhr',
                url: arguments[1],
                method: arguments[0],
                timestamp: new Date().toISOString()
            });
            return originalXHROpen.apply(this, arguments);
        };
        
        return "INTERCEPTORES ACTIVADOS";
        """
        
        d.execute_script(script_intercept)
        
        # Hacer click nuevamente
        boton.click()
        time.sleep(3)
        
        # Verificar peticiones interceptadas
        requests = d.execute_script("return window.interceptedRequests;")
        print(f"   Peticiones interceptadas: {len(requests)}")
        for i, req in enumerate(requests or []):
            print(f"     [{i+1}] {req['type'].upper()} {req['method']} {req['url']}")
        
        # 7. GUARDAR HTML COMPLETO PARA ANÁLISIS
        print("\n5. GUARDANDO HTML PARA ANÁLISIS...")
        
        html_content = d.page_source
        
        # Guardar HTML completo
        with open("diagnostico_formulario_completo.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        
        # Extraer solo el formulario
        import re
        form_match = re.search(r'(<form[^>]*>.*?</form>)', html_content, re.DOTALL)
        
        if form_match:
            with open("diagnostico_solo_formulario.html", "w", encoding="utf-8") as f:
                f.write(form_match.group(1))
            print("   ✅ Formulario guardado en: diagnostico_solo_formulario.html")
        
        print("\n" + "="*80)
        print("DIAGNÓSTICO COMPLETADO")
        print("="*80)
        
        # Mostrar conclusión
        print("\n📋 CONCLUSIÓN DEL DIAGNÓSTICO:")
        
        if requests and len(requests) > 0:
            print("✅ El formulario SÍ hace peticiones HTTP")
            for req in requests:
                if req['method'].upper() == 'POST':
                    print("   ✅ Hay petición POST")
                    print(f"   URL: {req['url']}")
        else:
            print("❌ El formulario NO hace peticiones HTTP")
            print("   Posibles causas:")
            print("   1. El botón no es type='submit' realmente")
            print("   2. JavaScript está previniendo el submit")
            print("   3. Hay event listeners que cancelan el evento")
        
        action = formulario.get_attribute('action')
        if not action or action == "":
            print("⚠️  El formulario tiene action vacío")
            print("   Esto puede causar problemas con el envío")
        
        print("\n📁 Archivos generados:")
        print("   - diagnostico_formulario_completo.html (HTML completo)")
        print("   - diagnostico_solo_formulario.html (Solo formulario)")
        print("   - diagnostico_antes_submit.png (Screenshot)")
    
    def test_solucion_definitiva(self):
        """Solución DEFINITIVA: Enviar POST directamente"""
        print("\n" + "="*80)
        print("SOLUCIÓN DEFINITIVA")
        print("="*80)
        
        from apps.rutas.models import Ruta
        
        # Estado inicial
        rutas_inicial = Ruta.objects.count()
        print(f"Rutas iniciales: {rutas_inicial}")
        
        d = self.driver
        
        # Login
        d.get(self.live_server_url + "/accounts/login/")
        time.sleep(2)
        
        d.find_element(By.ID, "id_username").send_keys(self.user.username)
        d.find_element(By.ID, "id_password").send_keys(self.password + Keys.RETURN)
        time.sleep(3)
        
        # Ir a rutas para obtener CSRF token y URL correcta
        d.get(self.live_server_url + "/rutas/crear/")
        time.sleep(3)
        
        # Obtener URL actual (por si hay parámetros GET)
        current_url = d.current_url
        print(f"URL actual: {current_url}")
        
        # Extraer path sin parámetros
        from urllib.parse import urlparse
        parsed_url = urlparse(current_url)
        post_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
        print(f"URL para POST: {post_url}")
        
        # Obtener CSRF token
        csrf_token = d.execute_script("""
            var input = document.querySelector('input[name="csrfmiddlewaretoken"]');
            return input ? input.value : '';
        """)
        
        print(f"CSRF token: {csrf_token[:30]}...")
        
        # Enviar POST DIRECTAMENTE con fetch
        hoy = timezone.now().date().strftime("%Y-%m-%d")
        
        script_post = f"""
        // Enviar POST directamente
        var formData = new FormData();
        formData.append('doctor_id', '{self.doctor.id}');
        formData.append('fecha_visita', '{hoy}');
        
        if ('{csrf_token}') {{
            formData.append('csrfmiddlewaretoken', '{csrf_token}');
        }}
        
        console.log('Enviando POST a:', '{post_url}');
        console.log('Datos:', {{
            doctor_id: '{self.doctor.id}',
            fecha_visita: '{hoy}',
            csrf_token: '{csrf_token[:20]}...'
        }});
        
        fetch('{post_url}', {{
            method: 'POST',
            body: formData,
            headers: {{
                'Accept': 'text/html,application/xhtml+xml,application/xml',
                'X-Requested-With': 'XMLHttpRequest'
            }}
        }})
        .then(response => {{
            console.log('Response status:', response.status);
            console.log('Response headers:', Object.fromEntries(response.headers.entries()));
            
            if (response.redirected) {{
                console.log('Redireccionando a:', response.url);
                window.location.href = response.url;
            }} else {{
                return response.text();
            }}
        }})
        .then(data => {{
            if (data) {{
                console.log('Response length:', data.length);
                // Reemplazar contenido de la página
                document.open();
                document.write(data);
                document.close();
            }}
        }})
        .catch(error => {{
            console.error('Error:', error);
        }});
        
        return 'POST ENVIADO';
        """
        
        print("\nEnviando POST directo...")
        resultado = d.execute_script(script_post)
        print(f"Resultado: {resultado}")
        
        # Esperar
        print("Esperando respuesta...")
        time.sleep(5)
        
        # Verificar
        rutas_final = Ruta.objects.count()
        print(f"\nRutas finales: {rutas_final}")
        
        if rutas_final > rutas_inicial:
            print("✅ ¡RUTA CREADA CON ÉXITO!")
            ruta = Ruta.objects.last()
            print(f"   ID: {ruta.id}")
            print(f"   Doctor: {ruta.doctor.nombre}")
            print(f"   Fecha: {ruta.fecha_visita}")
            print(f"   Estatus: {ruta.estatus}")
        else:
            print("❌ POST directo no funcionó")
            
            # Debug: ver página actual
            print(f"\nURL actual: {d.current_url}")
            print(f"Título: {d.title}")
            
            # Verificar si hay mensajes
            try:
                alertas = d.find_elements(By.CSS_SELECTOR, ".alert")
                if alertas:
                    print(f"Mensajes encontrados: {len(alertas)}")
                    for alerta in alertas:
                        print(f"  - {alerta.text}")
            except:
                pass
            
            # Guardar HTML
            with open("solucion_definitiva_error.html", "w", encoding="utf-8") as f:
                f.write(d.page_source)
            print("HTML guardado en solucion_definitiva_error.html")
        
        self.assertGreater(rutas_final, rutas_inicial, 
                          f"Rutas deberían aumentar. Inicial: {rutas_inicial}, Final: {rutas_final}")
        
        print("\n" + "="*80)
        print("SOLUCIÓN COMPLETADA")
        print("="*80)