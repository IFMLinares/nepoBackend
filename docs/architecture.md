# Arquitectura del Proyecto

NepoBackend utiliza un enfoque de **Arquitectura Limpia** simplificada mediante el patrón **Service Layer**.

## 1. Service Layer (Capa de Servicio)

Toda la lógica de negocio se encuentra en los archivos `services.py` de cada aplicación. 

- **Propósito:** Mantener las vistas (`views.py`) delgadas y enfocadas solo en la gestión de peticiones HTTP y respuestas.
- **Transacciones:** Los servicios utilizan `@transaction.atomic` para asegurar la integridad de los datos (ej: al crear un Usuario, se debe crear obligatoriamente su Perfil).

## 2. Autenticación Híbrida

El sistema está diseñado para ser consumido tanto por clientes Web (React) como Móviles (React Native).

### Flujo Web
- El login deposita los tokens (`access_token` y `refresh_token`) en **Cookies HttpOnly**.
- Esto previene ataques XSS ya que el JavaScript del navegador no puede leer los tokens.
- El Middleware de Django extrae automáticamente los tokens de las cookies.

### Flujo Móvil
- El login devuelve los tokens en el cuerpo de la respuesta JSON.
- El cliente móvil debe guardar estos tokens y enviarlos en el header `Authorization: Bearer <token>`.

## 2. Selectors (Capa de Consultas)

Para mantener las consultas complejas y optimizadas (usando `select_related` y `prefetch_related`) fuera de las vistas y servicios.
- **Propósito:** Encapsular la lógica de filtrado y acceso a datos.

## 3. Autenticación Híbrida
... (resto del contenido) ...

## 4. Estructura de Aplicaciones

- **core/**: Contiene los ajustes globales, configuración de JWT, CORS y la documentación OpenAPI.
- **apps/users/**: Gestión de identidad, perfiles y roles.
- **apps/payments/**: Manejo dinámico de monedas y métodos de pago.
- **apps/inventory/**: Control de stock, categorías y unidades con soporte multimedia.
- **apps/common/**: Clases base (TimestampedModel) y utilidades.
