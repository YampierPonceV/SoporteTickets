# Documentación de la API

## Base URL

```
https://127.0.0.1:5000
```

---

## Autenticación

### 1. Requerimientos de autenticación

Todas las peticiones a la API, tales como `GET`, `POST`, `PUT`, `DELETE`, y similares, requieren que el usuario esté autenticado y que se incluya un **token de acceso** en la cabecera de la solicitud. Este token se obtiene al iniciar sesión con las credenciales del usuario.

### 2. Obtener el token de acceso

- **URL para login:** `/login`
- **Método:** `POST`
- **Descripción:** Permite al usuario iniciar sesión y obtener un token de acceso.
- **Cuerpo de la solicitud:**
  - `usuario` (requerido): El nombre de usuario.
  - `contraseña` (requerido): La contraseña del usuario.

**Respuesta exitosa:**

```json
{
  "token": "tu_token_de_acceso_aqui"
}
```

Este token debe ser incluido en la cabecera de cada solicitud subsecuente como parte de la autenticación:

- **Cabecera de la solicitud:**
  ```
  Authorization: Bearer <tu_token_de_acceso_aqui>
  ```

---

## Endpoints de Usuarios

### 1. Obtener todos los usuarios

- **URL:** `/api/usuarios`
- **Método:** `GET`
- **Descripción:** Recupera la lista de todos los usuarios.
- **Requiere autenticación:** Sí (token de acceso en la cabecera).

### 2. Obtener un usuario por DNI

- **URL:** `/api/usuarios/dni/<numero_dni>`
- **Método:** `GET`
- **Descripción:** Obtiene los detalles de un usuario específico mediante su número de DNI.
- **Parámetros:**
  - `numero_dni` (requerido): El DNI del usuario que deseas consultar.
- **Requiere autenticación:** Sí (token de acceso en la cabecera).

### 3. Crear un nuevo usuario

- **URL:** `/api/usuarios/crear_usuarios`
- **Método:** `POST`
- **Descripción:** Crea un nuevo usuario.
- **Cuerpo de la solicitud:**
  - Datos del nuevo usuario (ej., nombre, DNI, correo, etc.).
- **Requiere autenticación:** Sí (token de acceso en la cabecera).

### 4. Soporte de usuario

- **URL:** `/api/usuarios/soporte-ti`
- **Método:** `GET`
- **Descripción:** Recupera información de soporte técnico para los usuarios.
- **Requiere autenticación:** Sí (token de acceso en la cabecera).

---

## Endpoints de Tickets

### 5. Obtener todos los tickets

- **URL:** `/api/tickets`
- **Método:** `GET`
- **Descripción:** Recupera la lista de todos los tickets.
- **Requiere autenticación:** Sí (token de acceso en la cabecera).

### 6. Obtener un ticket por ID

- **URL:** `/api/tickets/id/<ticket_id>`
- **Método:** `GET`
- **Descripción:** Obtiene los detalles de un ticket específico por su ID.
- **Parámetros:**
  - `ticket_id` (requerido): El ID del ticket que deseas consultar.
- **Requiere autenticación:** Sí (token de acceso en la cabecera).

### 7. Obtener los tickets por el DNI del usuario

- **URL:** `/api/tickets/usuarios/dni/<dni>`
- **Método:** `GET`
- **Descripción:** Obtiene los tickets asociados a un usuario mediante su DNI.
- **Parámetros:**
  - `dni` (requerido): El DNI del usuario cuyos tickets deseas consultar.
- **Requiere autenticación:** Sí (token de acceso en la cabecera).

### 8. Crear un nuevo ticket

- **URL:** `/api/tickets/crear_ticket`
- **Método:** `POST`
- **Descripción:** Crea un nuevo ticket.
- **Cuerpo de la solicitud:**
  - Datos del ticket (ej., descripción, prioridad, etc.).
- **Requiere autenticación:** Sí (token de acceso en la cabecera).

### 9. Obtener tickets sin atender

- **URL:** `/api/tickets/sin-atender`
- **Método:** `GET`
- **Descripción:** Recupera los tickets que aún no han sido atendidos.
- **Requiere autenticación:** Sí (token de acceso en la cabecera).

### 10. Actualizar un ticket

- **URL:** `/api/tickets/actualizar/id/<ticket_id>`
- **Método:** `PUT`
- **Descripción:** Actualiza los detalles de un ticket existente.
- **Parámetros:**
  - `ticket_id` (requerido): El ID del ticket que deseas actualizar.
- **Cuerpo de la solicitud:**
  - Datos a actualizar (ej., estado, descripción, etc.).
- **Requiere autenticación:** Sí (token de acceso en la cabecera).

### 11. Atender un ticket

- **URL:** `/api/atenciontickets`
- **Método:** `POST`
- **Descripción:** Permite atender un ticket.
- **Cuerpo de la solicitud:**
  - Detalles sobre cómo se atendió el ticket (ej., resolución, comentarios, etc.).
- **Requiere autenticación:** Sí (token de acceso en la cabecera).

---

## Endpoint de Login

### 12. Login de usuario

- **URL:** `/login`
- **Método:** `POST`
- **Descripción:** Permite a un usuario iniciar sesión en el sistema y obtener un token de acceso.
- **Cuerpo de la solicitud:**
  - `usuario` (requerido): El nombre de usuario.
  - `contraseña` (requerido): La contraseña del usuario.

**Respuesta exitosa:**

```json
{
  "token": "tu_token_de_acceso_aqui"
}
```

---

## Notas adicionales

- Asegúrate de que todas las peticiones `POST`, `PUT`, `GET`, etc., incluyan el token de autenticación en la cabecera.
- El token debe ser enviado en la cabecera de la solicitud como sigue:
  ```
  Authorization: Bearer <tu_token_de_acceso_aqui>
  ```
- Todos los endpoints requieren el uso de HTTPS para garantizar la seguridad de las comunicaciones.
