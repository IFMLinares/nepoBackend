# NepoBackend - API Deportiva 🚀

Backend robusto para la plataforma Nepo, diseñado para aplicaciones móviles y web. Desarrollado con Django Rest Framework, siguiendo una arquitectura de **Service Layer** y un sistema de autenticación híbrida seguro.

## 🛠️ Tecnologías

- **Lenguaje:** Python 3.13+
- **Framework:** Django 6.0.4
- **API:** Django Rest Framework (DRF)
- **Autenticación:** SimpleJWT (JWT + Cookies HttpOnly)
- **Documentación:** OpenAPI 3.0 con `drf-spectacular`
- **Multimedia:** Pillow (Procesamiento de imágenes)
- **Base de Datos:** SQLite (Desarrollo) / PostgreSQL (Recomendado para Producción)
- **Testing:** Pytest & Pytest-Django

## 📂 Estructura del Proyecto

```text
nepoBackend/
├── apps/               
│   ├── users/          # Gestión de usuarios y perfiles
│   ├── payments/       # Módulo de pagos y tipos de cambio
│   ├── inventory/      # Módulo de productos y categorías
│   └── common/         # Utilidades compartidas
├── core/               # Configuración central (Settings, URLs)
├── media/              # Archivos subidos (Imágenes)
├── docs/               # Documentación detallada
├── manage.py           # Gestor de Django
└── pytest.ini          # Configuración de tests
```

## 🚀 Instalación y Configuración

### 1. Clonar y preparar entorno
```powershell
# Crear entorno virtual
python -m venv venv

# Activar entorno
.\venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Base de Datos y Migraciones
```powershell
python manage.py makemigrations
python manage.py migrate
```

### 3. Crear Superusuario
```powershell
python manage.py createsuperuser
```

### 4. Ejecutar Servidor
```powershell
python manage.py runserver
```

## 🧪 Testing

El proyecto utiliza `pytest` para asegurar la calidad del código.

```powershell
# Ejecutar todos los tests
.\venv\Scripts\pytest.exe
```

## 📖 Documentación de la API

Una vez que el servidor esté corriendo, puedes acceder a la documentación interactiva en:

- **Swagger UI:** [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)
- **Redoc:** [http://localhost:8000/api/redoc/](http://localhost:8000/api/redoc/)

---
Para más detalles sobre la arquitectura y modelos, revisa la carpeta [`/docs`](./docs/).
