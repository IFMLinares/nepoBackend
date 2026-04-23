# Modelos de Datos

El sistema centraliza la identidad en la aplicación `users`.

## 1. User (Usuario Personalizado)

Hereda de `AbstractBaseUser` y `PermissionsMixin`.

- **Campos:**
    - `username`: Nombre único para login.
    - `email`: Correo electrónico (único).
    - `role`: Campo `TextChoices` que define el nivel de acceso (`ADMIN`, `COACH`, `REPRESENTATIVE`, `STUDENT`).
    - `is_active`: Estado de la cuenta.
    - `is_staff`: Acceso al panel administrativo.

## 2. Profile (Perfil de Usuario)

Extensión de la información del usuario mediante una relación `OneToOne`.

- **Campos:**
    - `full_name`: Nombre completo del deportista o representante.
    - `identification`: Cédula de identidad o pasaporte (único).
    - `phone_number`: Teléfono de contacto.
    - `representative`: Relación recursiva (`FK` a `Profile`) que vincula a un `Estudiante` con su `Representante`.

## 3. Roles y Permisos

Los roles están integrados en el código para máxima eficiencia:

| Rol | Slug | Descripción |
| :--- | :--- | :--- |
| Administrador | `ADMIN` | Control total del sistema. |
| Entrenador | `COACH` | Gestión de atletas y entrenamientos. |
| Representante | `REPRESENTATIVE` | Tutores legales de los estudiantes. |
| Estudiante | `STUDENT` | Deportistas de la plataforma. |
