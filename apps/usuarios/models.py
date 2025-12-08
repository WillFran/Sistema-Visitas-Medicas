# apps/usuarios/models.py
from django.contrib.auth.models import AbstractUser  # 👈 IMPORTANTE
from django.db import models


class Usuario(AbstractUser):
    # Valores internos SIEMPRE en minúsculas
    ROL_VISITADOR = "visitador"
    ROL_SUPERVISOR = "supervisor"

    ROLES = (
        (ROL_VISITADOR, "Visitador médico"),
        (ROL_SUPERVISOR, "Supervisor"),
    )

    rol = models.CharField(
        max_length=20,
        choices=ROLES,
        null=True,
        blank=True,
    )

    must_change_password = models.BooleanField(
        default=False
    )  # por defecto False

    def save(self, *args, **kwargs):
        # Normalizar el rol a minúsculas por seguridad
        if self.rol:
            self.rol = self.rol.lower().strip()

        # Solo obliga a cambiar contraseña si es usuario NUEVO
        # y NO es superuser ni staff (tu lógica original)
        if not self.pk and not self.is_superuser and not self.is_staff:
            self.must_change_password = True

        super().save(*args, **kwargs)