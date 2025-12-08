# apps/usuarios/tests.py

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from django.test import override_settings

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from apps.usuarios.models import Usuario

import time


@override_settings(DEBUG=True)
class LoginFunctionalTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def setUp(self):
        self.password = "Testpass123"
        self.email = "admin_funcional@test.com"

        # ⚠️ IMPORTANTE: username = email, porque así se loguean en tu sistema
        self.user = Usuario.objects.create_superuser(
            username=self.email,
            email=self.email,
            password=self.password,
            rol="SUPERVISOR",  # opcional, pero útil para tus vistas
        )

    def test_login_exitoso_muestra_pantalla_inicio(self):
        login_url = self.live_server_url + reverse("login")
        self.driver.get(login_url)

        username_input = self.driver.find_element(By.NAME, "username")
        password_input = self.driver.find_element(By.NAME, "password")

        # El formulario dice "Correo electrónico", pero el campo se llama "username"
        username_input.send_keys(self.email)
        password_input.send_keys(self.password)
        password_input.send_keys(Keys.RETURN)

        # Esperamos un poco para que redirija
        time.sleep(1)

        page = self.driver.page_source

        # Confirmamos que NO haya mensaje de error
        self.assertNotIn("Usuario o contraseña incorrectos", page)

        # Y que sí estemos en el dashboard
        self.assertIn("Bienvenido", page)
        self.assertIn("Registrar Asistencia", page)
        self.assertIn("Gestionar Visitas Médicas", page)

        # Para que puedas ver el navegador
        time.sleep(5)