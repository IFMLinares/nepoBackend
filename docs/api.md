# Documentación de la API

La API sigue los principios REST y utiliza JSON como formato de intercambio.

## 🔑 Autenticación

Todos los endpoints (excepto `/register` y `/login`) requieren autenticación.

### Endpoints de Auth

| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| `POST` | `/api/users/register/` | Registro de nuevos usuarios. |
| `POST` | `/api/users/login/` | Obtención de tokens (JSON + Cookies). |
| `POST` | `/api/users/token/refresh/` | Refrescar el token de acceso. |
| `POST` | `/api/users/logout/` | Limpiar cookies de sesión. |
| `GET` | `/api/users/me/` | Datos del usuario actual. |

## 🛡️ Clases de Permiso

En `apps/users/permissions.py` existen clases listas para usar:

- `IsAdmin`: Solo para roles `ADMIN`.
- `IsCoach`: Solo para roles `COACH`.
- `IsRepresentative`: Solo para roles `REPRESENTATIVE`.
- `IsStudent`: Solo para roles `STUDENT`.

### Ejemplo de uso en vistas:
```python
from apps.users.permissions import IsCoach

class EntrenamientoView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsCoach]
    ...
```

## 🛠️ Documentación Interactiva

El sistema genera automáticamente el esquema OpenAPI 3.0.

- **Swagger:** Interfaz visual para probar endpoints.
- **Redoc:** Documentación técnica detallada.
