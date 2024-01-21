
# README.md

## API de Pizza

Esta API permite a los usuarios gestionar pizzas e ingredientes, incluyendo la capacidad de agregar o eliminar ingredientes de las pizzas.

### Configuración del Entorno

#### Requisitos Previos
- Python 3.x
- Django y Django Rest Framework
- Un cliente API como Postman o cURL

#### Instalación y Ejecución
1. Clona el repositorio del proyecto.
2. Crea y activa el venv
3. Instala las dependencias: `pip install -r requirements.txt`.
4. cd pizza_backend
5. Prepara las migraciones: `py manage.py makemigrations`
5. Realiza las migraciones: `py manage.py migrate`.
6. Inicia el servidor: `py manage.py runserver`.

### Autenticación

#### Registro de Usuarios
- **Endpoint**: `/register/`
- **Método**: POST
- **Cuerpo de la Solicitud**: `{"username": "user", "password": "pass", "user_type": "normal/staff"}`
- **Respuesta**: Detalles del usuario registrado.

#### Iniciar Sesión y Obtener Token
- **Endpoint**: `/api-token-auth/`
- **Método**: POST
- **Cuerpo de la Solicitud**: `{"username": "user", "password": "pass"}`
- **Respuesta**: Token de autenticación.

#### Uso del Token
Agrega el token a la cabecera de tus solicitudes para acceder a los endpoints protegidos:
```
Authorization: Token <tu_token>
```

### Endpoints

#### Pizza

##### Listar Pizzas
- **Endpoint**: `/pizzas/`
- **Método**: GET
- **Permisos**: Cualquiera (solo activas para no staff)

##### Detalles de Pizza
- **Endpoint**: `/pizzas/<id>/`
- **Método**: GET, PUT, DELETE
- **Permisos**: Solo staff

#### Ingredientes

##### Listar Ingredientes
- **Endpoint**: `/ingredients/`
- **Método**: GET, POST
- **Permisos**: Solo staff

##### Detalles de Ingrediente
- **Endpoint**: `/ingredients/<id>/`
- **Método**: GET, PUT, DELETE
- **Permisos**: Solo staff
- **Nota**: No se puede eliminar si está en una pizza activa.

#### Asociar Ingredientes a Pizza

##### Agregar Ingredientes
- **Endpoint**: `/pizzas/<pizza_id>/add_ingredients/`
- **Método**: POST
- **Cuerpo de la Solicitud**: `{"ingredients": [id1, id2]}`
- **Permisos**: Solo staff

##### Quitar Ingredientes
- **Endpoint**: `/pizzas/<pizza_id>/remove_ingredients/`
- **Método**: POST
- **Cuerpo de la Solicitud**: `{"ingredients": [id1, id2]}`
- **Permisos**: Solo staff

### Realizar Pruebas

Utiliza un cliente API como Postman para probar los endpoints. Asegúrate de incluir el token de autenticación en las cabeceras para los endpoints protegidos.
