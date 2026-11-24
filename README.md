# Sistema de Visitas Médicas

Aplicación web desarrollada con **Python y Django** para trabajar con información relacionada con visitas médicas. El repositorio reúne el backend, las plantillas HTML y los archivos estáticos de la interfaz.

Este proyecto forma parte de mi portafolio de desarrollo web. Me permitió trabajar con la organización de una aplicación Django, la integración entre vistas y plantillas y el manejo del código en Git.

## Tecnologías

- **Python y Django:** estructura y lógica del servidor.
- **HTML, CSS y JavaScript:** plantillas y comportamiento de la interfaz.
- **Git y GitHub:** control de versiones.

El repositorio también incluye archivos de configuración para despliegue (`Procfile` y `docker-compose.yml`). Su presencia no implica que exista una versión pública desplegada.

## Organización del proyecto

```text
Sistema-Visitas-Medicas/
├── apps/               # Aplicaciones del proyecto Django
├── static/             # CSS, JavaScript y otros recursos estáticos
├── templates/          # Plantillas HTML
├── visitas_medicas/    # Configuración principal de Django
├── manage.py           # Comandos de administración de Django
├── requirements.txt    # Dependencias de Python
├── pyproject.toml      # Configuración del proyecto
├── docker-compose.yml  # Configuración de contenedores
└── Procfile            # Configuración de ejecución/despliegue
```

## Ejecución local

Para revisar el proyecto en un entorno local:

1. Clonar el repositorio:

   ```bash
   git clone https://github.com/WillFran/Sistema-Visitas-Medicas.git
   cd Sistema-Visitas-Medicas
   ```

2. Crear y activar un entorno virtual:

   **Windows (PowerShell)**

   ```powershell
   py -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

   **Linux/macOS**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Instalar las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

4. Revisar la configuración de base de datos y las variables de entorno requeridas por `visitas_medicas/settings.py`. Una vez configuradas, aplicar las migraciones y ejecutar el servidor:

   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

5. Abrir `http://127.0.0.1:8000/`.

> **Nota:** estos son los pasos habituales de un proyecto Django. Dependiendo de la configuración de la base de datos y los servicios utilizados, puede ser necesario realizar ajustes adicionales antes de ejecutar la aplicación.

## Estado del repositorio

Es un proyecto de portafolio y aprendizaje práctico. El código se comparte para mostrar su organización y las tecnologías utilizadas; no se presenta como un producto clínico validado ni como un sistema listo para producción.

## Capturas de pantalla

Se incorporarán capturas de las pantallas principales una vez revisadas para evitar publicar información personal o de pacientes.

## Autor

**Willy Francis Delgado**  
GitHub: [@WillFran](https://github.com/WillFran)
