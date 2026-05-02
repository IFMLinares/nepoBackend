# Testing con Pytest

El proyecto utiliza un enfoque de pruebas automatizadas para garantizar que la API reporte errores correctamente y no se rompa ante datos inválidos.

## ⚙️ Configuración

- **Framework:** `pytest`
- **Plugin:** `pytest-django`
- **Config:** `pytest.ini` en la raíz.

## 🏃 Cómo ejecutar los tests

```powershell
# Ejecutar todos los tests
.\venv\Scripts\pytest.exe

# Ejecutar con detalles
.\venv\Scripts\pytest.exe -v

# Ejecutar un archivo específico
.\venv\Scripts\pytest.exe apps/users/tests/test_auth.py
```

## 📝 Cobertura de Pruebas

Actualmente, las pruebas en `apps/users/tests/` cubren:

1.  **Registro:** Casos de éxito, duplicados de nombre de usuario/email y validaciones de contraseña.
2.  **Login:** Verificación de credenciales y creación de cookies HttpOnly.
3.  **Seguridad:** Bloqueo de rutas protegidas para usuarios no autenticados.
4.  **Roles:** Verificación de que el serializador devuelve el rol correcto.
5.  **Inventario:** Creación de productos, subida de imágenes, filtrado por categoría y borrado lógico (soft delete).

## 💡 Mejores Prácticas

- Usa el fixture `client` proporcionado por `pytest-django`.
- Marca los tests que requieren base de datos con `@pytest.mark.django_db`.
- Prueba siempre el "Happy Path" (éxito) y los "Edge Cases" (errores esperados).
