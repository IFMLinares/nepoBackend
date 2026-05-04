from django.db import transaction
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

class UserService:
    @staticmethod
    @transaction.atomic
    def register_user(username, email, password, full_name, identification, role=User.Role.STUDENT, **extra_profile_fields):
        """
        Registra un nuevo usuario con su rol y perfil asociado.
        """
        # Crear usuario con su rol
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role
        )

        # Actualizar perfil (que debería haber sido creado por la señal, o lo creamos aquí)
        Profile.objects.update_or_create(
            user=user,
            defaults={
                'full_name': full_name,
                'identification': identification,
                **extra_profile_fields
            }
        )

        return user
