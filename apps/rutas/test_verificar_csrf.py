# En tu tests.py, actualiza el test TestCSRFVerification:

class TestCSRFVerification(StaticLiveServerTestCase):
    """Tests para verificar que CSRF está desactivado"""
    
    def test_csrf_en_testing(self):
        """Verificar configuración de testing"""
        print("\n" + "="*60)
        print("VERIFICANDO CONFIGURACIÓN DE TESTING")
        print("="*60)
        
        # Verificar que estamos en modo testing
        import sys
        self.assertIn('test', sys.argv, "No estamos en modo testing")
        print("✅ Estamos en modo testing")
        
        # Verificar que DEBUG está activo
        from django.conf import settings
        print(f"DEBUG en settings: {settings.DEBUG}")
        print(f"TEMPLATE_DEBUG en settings: {getattr(settings, 'TEMPLATE_DEBUG', 'No definido')}")
        
        # DEBUG debería ser True (lo forzamos en settings)
        self.assertTrue(settings.DEBUG, 
                       f"DEBUG debería ser True en testing, pero es {settings.DEBUG}")
        print("✅ DEBUG está en True")
        
        # Verificar que CSRF middleware no está
        middlewares = list(settings.MIDDLEWARE)
        csrf_middleware = 'django.middleware.csrf.CsrfViewMiddleware'
        
        print(f"\nMiddleware activos ({len(middlewares)}):")
        for i, m in enumerate(middlewares, 1):
            print(f"  {i:2}. {m}")
        
        self.assertNotIn(csrf_middleware, middlewares, 
                        f"CSRF middleware aún está activo: {csrf_middleware}")
        print("✅ CSRF middleware desactivado")
        
        # Verificar configuración CSRF
        print(f"\nConfiguración CSRF:")
        print(f"  - CSRF_COOKIE_SECURE: {settings.CSRF_COOKIE_SECURE}")
        print(f"  - CSRF_COOKIE_HTTPONLY: {settings.CSRF_COOKIE_HTTPONLY}")
        print(f"  - CSRF_USE_SESSIONS: {settings.CSRF_USE_SESSIONS}")
        
        self.assertFalse(settings.CSRF_COOKIE_SECURE, 
                        "CSRF_COOKIE_SECURE debería ser False")
        self.assertFalse(settings.CSRF_COOKIE_HTTPONLY,
                        "CSRF_COOKIE_HTTPONLY debería ser False")
        print("✅ Configuración CSRF correcta")
        
        print("\n" + "="*60)
        print("CONFIGURACIÓN DE TESTING VERIFICADA ✅")
        print("="*60)
    
    def test_post_sin_csrf_funciona(self):
        """Verificar que POST sin CSRF token funciona"""
        print("\n" + "="*60)
        print("TEST: POST SIN CSRF TOKEN")
        print("="*60)
        
        # Crear usuario y doctor para el test
        User = get_user_model()
        user = User.objects.create_user(
            username="post_test@test.com",
            password="Test1234*",
            rol="VISITADOR",
            is_staff=True,
        )
        
        # Crear doctor
        dep = Departamento.objects.create(nombre="TEST")
        prov = Provincia.objects.create(nombre="TEST", departamento=dep)
        dist = Distrito.objects.create(nombre="TEST", provincia=prov)
        
        doctor = Doctor.objects.create(
            cmp="999999",
            nombre="Doctor POST Test",
            apellido="Test",
            especialidad="M.G.",
            direccion="Test 123",
            ubigeo=dist,
            visitador=user,
        )
        
        # Usar Client de Django (no Selenium)
        from django.test import Client
        client = Client()
        
        # Forzar login
        client.force_login(user)
        
        # Hacer POST sin CSRF token
        print("\n1. Haciendo POST sin CSRF token...")
        response = client.post('/rutas/crear/', {
            'doctor_id': str(doctor.id),
            'fecha_visita': '2025-12-04'
        }, follow=True)  # follow=True para seguir redirecciones
        
        print(f"   Status code final: {response.status_code}")
        
        # Verificar que NO es 403 (Forbidden por CSRF)
        self.assertNotEqual(response.status_code, 403, 
                           "❌ POST bloqueado por CSRF (status 403)")
        
        # Verificar que no es 500 (Error del servidor)
        self.assertNotEqual(response.status_code, 500,
                           "❌ Error 500 del servidor")
        
        # Status debería ser 200 (después de redirect) o 302 (redirect)
        acceptable_statuses = [200, 302]
        self.assertIn(response.status_code, acceptable_statuses,
                     f"❌ Status inesperado: {response.status_code}")
        
        print(f"✅ POST aceptado (status {response.status_code})")
        
        # Verificar mensajes
        if hasattr(response, 'context') and 'messages' in response.context:
            messages = list(response.context['messages'])
            for msg in messages:
                print(f"   Mensaje: {msg}")
        
        print("\n" + "="*60)
        print("POST SIN CSRF FUNCIONA ✅")
        print("="*60)