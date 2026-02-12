# Guía de Estudio - Horios OTT

## 📚 Índice
1. [Introducción al Proyecto](#introducción-al-proyecto)
2. [Tecnologías Utilizadas](#tecnologías-utilizadas)
3. [Estructura del Proyecto](#estructura-del-proyecto)
4. [Por Qué FastAPI y Python](#por-qué-fastapi-y-python)
5. [Conexión con la Base de Datos](#conexión-con-la-base-de-datos)
6. [Integración con Mux](#integración-con-mux)
7. [Arquitectura y Flujo de Datos](#arquitectura-y-flujo-de-datos)
8. [Descripción de Cada Archivo](#descripción-de-cada-archivo)

---

## 🎯 Introducción al Proyecto

**Horios OTT** es una plataforma de streaming de video tipo OTT (Over-The-Top), similar a Netflix o YouTube. El proyecto permite:
- Subir y gestionar videos
- Autenticación de usuarios (JWT)
- Diferentes roles de usuario (USER, PREMIUM, ADMIN)
- Procesamiento y streaming de videos mediante Mux
- Panel de administración para gestionar usuarios

---

## 🛠️ Tecnologías Utilizadas

### Backend
- **FastAPI 0.104.1**: Framework web moderno y rápido
- **Python 3.x**: Lenguaje de programación principal
- **Uvicorn**: Servidor ASGI para ejecutar FastAPI
- **SQLAlchemy 2.0.23**: ORM para interactuar con la base de datos
- **PostgreSQL**: Base de datos relacional (via Supabase)
- **Alembic 1.13.0**: Herramienta para migraciones de base de datos

### Autenticación y Seguridad
- **python-jose[cryptography] 3.3.0**: Manejo de tokens JWT
- **passlib[bcrypt] 1.7.4**: Hash de contraseñas
- **bcrypt 3.2.2**: Algoritmo de hashing seguro
- **OAuth2PasswordBearer**: Esquema de autenticación

### Video Streaming
- **mux-python 5.1.2**: SDK para integración con Mux
- **Mux Video API**: Servicio de procesamiento y streaming de video

### Frontend
- **HTML5 + JavaScript vanilla**: Interfaz web
- **HLS.js**: Librería para reproducción de video HLS
- **CSS3**: Estilos personalizados

### Utilidades
- **pydantic 2.5.0**: Validación de datos
- **pydantic-settings 2.1.0**: Gestión de configuración
- **python-dotenv 1.0.0**: Carga de variables de entorno
- **requests 2.31.0**: Cliente HTTP
- **python-multipart 0.0.6**: Manejo de formularios multipart

---

## 📁 Estructura del Proyecto

```
Horios-OTT/
│
├── app/                          # Código principal de la aplicación
│   ├── __init__.py              # Inicialización del módulo
│   ├── auth/                    # Módulo de autenticación
│   │   ├── __init__.py
│   │   ├── router.py           # Rutas de auth (login, register)
│   │   ├── schemas.py          # Modelos Pydantic para validación
│   │   ├── security.py         # Hash de contraseñas y JWT
│   │   └── deps.py             # Dependencias (get_current_user)
│   │
│   ├── admin/                   # Módulo de administración
│   │   ├── __init__.py
│   │   ├── router.py           # Rutas admin (gestión usuarios)
│   │   └── schemas.py          # Modelos para admin
│   │
│   ├── videos/                  # Módulo de videos
│   │   ├── __init__.py
│   │   ├── router.py           # CRUD de videos y reproducción
│   │   └── schemas.py          # Modelos de videos
│   │
│   ├── mux/                     # Integración con Mux
│   │   ├── __init__.py
│   │   └── service.py          # Cliente para API de Mux
│   │
│   ├── core/                    # Configuración central
│   │   ├── __init__.py
│   │   └── config.py           # Settings y variables de entorno
│   │
│   └── db/                      # Base de datos
│       ├── __init__.py
│       ├── database.py         # Conexión y sesión de DB
│       └── models.py           # Modelos SQLAlchemy (User, Video)
│
├── migrations/                  # Migraciones SQL
│   ├── 001_initial_schema.sql  # Tablas iniciales
│   └── 002_add_is_hidden.sql   # Añade campo is_hidden
│
├── web/                         # Frontend HTML
│   ├── index.html              # Página principal (catálogo)
│   └── login.html              # Página de login/registro
│
├── scripts/                     # Scripts auxiliares
│
├── main.py                      # Punto de entrada de FastAPI
├── requirements.txt             # Dependencias Python
├── run_migrations.sh           # Script para ejecutar migraciones
├── setup.bat                   # Script de setup para Windows
├── .env.example                # Plantilla de variables de entorno
├── .gitignore                  # Archivos ignorados por Git
└── README.md                   # Documentación básica
```

---

## 💡 Por Qué FastAPI y Python

### ¿Por qué FastAPI?

1. **Alto Rendimiento**
   - FastAPI es uno de los frameworks más rápidos de Python
   - Comparable a Node.js y Go en velocidad
   - Ideal para APIs que manejan video y datos en tiempo real

2. **Documentación Automática**
   - Genera automáticamente documentación interactiva (Swagger UI)
   - Accesible en `/docs` - facilita el testing y desarrollo
   - Basado en OpenAPI estándar

3. **Validación de Datos Automática**
   - Usa Pydantic para validación de tipos
   - Detecta errores antes de procesar requests
   - Reduce código boilerplate

4. **Async/Await Nativo**
   - Soporte completo para programación asíncrona
   - Mejor manejo de operaciones I/O (DB, APIs externas)
   - Esencial para operaciones con Mux API

5. **Type Hints**
   - Python moderno con tipado estático
   - Mejor autocompletado en IDEs
   - Menos bugs en producción

6. **Facilidad de Integración**
   - Excelente soporte para ORMs (SQLAlchemy)
   - Middleware para CORS, autenticación, etc.
   - Gran ecosistema de librerías

### ¿Por qué Python?

1. **Ecosistema Rico**
   - Miles de librerías disponibles (ORMs, JWT, bcrypt, etc.)
   - SDKs oficiales para servicios como Mux
   - Comunidad activa y documentación abundante

2. **Sintaxis Clara y Legible**
   - Código más mantenible
   - Curva de aprendizaje suave
   - Ideal para equipos de desarrollo

3. **Versatilidad**
   - Backend web, scripts, procesamiento de datos
   - Mismo lenguaje para múltiples tareas
   - Facilita la integración de features futuras (ML, analytics)

4. **Productividad**
   - Desarrollo más rápido que lenguajes compilados
   - Menos líneas de código para lograr lo mismo
   - Ideal para MVPs y prototipos

---

## 🗄️ Conexión con la Base de Datos

### Arquitectura de Base de Datos

El proyecto usa **PostgreSQL** como base de datos, hospedada en **Supabase** (un servicio BaaS - Backend as a Service).

### Componentes Clave

#### 1. **Configuración (app/core/config.py)**

```python
class Settings(BaseSettings):
    database_url: str  # URL de conexión a PostgreSQL
    # ...
```

- Usa `pydantic-settings` para cargar variables de entorno
- `DATABASE_URL` se carga desde archivo `.env`
- Formato: `postgresql://user:password@host:port/database`

#### 2. **Motor de Base de Datos (app/db/database.py)**

```python
engine = create_engine(
    settings.database_url,
    echo=False,           # No imprimir SQL queries
    pool_pre_ping=True,   # Verificar conexión antes de usar
)
```

**Funciones:**
- `create_engine()`: Crea el motor de conexión a PostgreSQL
- `pool_pre_ping=True`: Verifica que la conexión esté viva antes de usarla
- `SessionLocal`: Factory para crear sesiones de base de datos

#### 3. **Sesiones de Base de Datos**

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

- **Patrón de Dependency Injection**: FastAPI inyecta la sesión en cada endpoint
- Asegura que la sesión se cierre automáticamente después de cada request
- Previene conexiones huérfanas

#### 4. **ORM - SQLAlchemy**

**Modelos (app/db/models.py):**

```python
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    # ...
```

**Beneficios del ORM:**
- No escribir SQL manualmente (más seguro contra SQL injection)
- Código más Pythonic y mantenible
- Migraciones automáticas con Alembic
- Relaciones entre tablas fáciles de definir

### Flujo de una Query

1. **Request llega a un endpoint**
2. **FastAPI inyecta sesión** via `Depends(get_db)`
3. **Endpoint ejecuta query**: `db.query(User).filter(...).first()`
4. **SQLAlchemy traduce a SQL** y ejecuta contra PostgreSQL
5. **Resultado se mapea a objetos Python**
6. **Sesión se cierra automáticamente**

### Migraciones

**Ubicación:** `migrations/*.sql`

- `001_initial_schema.sql`: Crea tablas `users` y `videos`
- `002_add_is_hidden.sql`: Añade campo `is_hidden` a videos

**Ejecución:**
```bash
./run_migrations.sh
```

Las migraciones aseguran que el schema de la BD evolucione de forma controlada.

---

## 🎥 Integración con Mux

### ¿Qué es Mux?

**Mux** es un servicio de infraestructura de video que maneja:
- **Encoding**: Convierte videos a múltiples formatos y resoluciones
- **Hosting**: Almacena los videos procesados
- **Delivery**: Entrega el video via CDN global
- **Streaming adaptativo**: HLS (HTTP Live Streaming)

### ¿Por Qué Usar Mux?

1. **Evita Complejidad Técnica**
   - No necesitas configurar FFmpeg, transcoders, CDN
   - Mux maneja toda la infraestructura de video

2. **Streaming Adaptativo Automático**
   - Mux crea múltiples versiones (480p, 720p, 1080p, etc.)
   - El player elige la mejor calidad según el ancho de banda

3. **CDN Global**
   - Videos se entregan desde servidores cercanos al usuario
   - Baja latencia y alta velocidad

4. **Thumbnails Automáticos**
   - Genera miniaturas del video automáticamente
   - URL: `https://image.mux.com/{playback_id}/thumbnail.jpg`

5. **Analytics**
   - Estadísticas de reproducción (opcional)
   - Calidad de experiencia del usuario

### Cómo Funciona la Integración

#### 1. **Configuración (app/core/config.py)**

```python
class Settings(BaseSettings):
    mux_token_id: str       # API Token ID
    mux_token_secret: str   # API Secret
```

Estas credenciales se obtienen desde el dashboard de Mux y se configuran en `.env`.

#### 2. **Cliente Mux (app/mux/service.py)**

```python
class MuxService:
    def __init__(self):
        self.base_url = "https://api.mux.com/video/v1"
        self.auth = (settings.mux_token_id, settings.mux_token_secret)
```

**Método: create_asset()**
```python
def create_asset(self, input_url: str) -> Tuple[str, str]:
    payload = {
        "input": [{"url": input_url}],
        "playback_policy": ["public"],
    }
    response = requests.post(f"{self.base_url}/assets", ...)
    # Retorna: (mux_asset_id, playback_id)
```

- **input_url**: URL del video original (ej: S3, Google Drive, etc.)
- **playback_policy**: `"public"` = sin autenticación requerida
- **mux_asset_id**: ID interno de Mux para el asset
- **playback_id**: ID público para reproducción

**Método: get_asset_status()**
```python
def get_asset_status(self, mux_asset_id: str) -> str:
    response = requests.get(f"{self.base_url}/assets/{mux_asset_id}", ...)
    return data.get("status", "processing")
```

Estados posibles:
- `processing`: Mux está procesando el video
- `ready`: Video listo para streaming
- `failed`: Error en el procesamiento

**Método: get_public_playback_url()**
```python
def get_public_playback_url(playback_id: str) -> str:
    return f"https://stream.mux.com/{playback_id}.m3u8"
```

- Retorna URL del playlist HLS (`.m3u8`)
- Este archivo contiene referencias a los chunks de video

#### 3. **Flujo de Subida de Video**

**Endpoint: POST /videos**

1. Admin proporciona `input_url` (URL del video original)
2. Backend llama `mux_service.create_asset(input_url)`
3. Mux descarga el video desde `input_url`
4. Mux comienza a procesar (encoding, chunking)
5. Mux retorna `mux_asset_id` y `playback_id`
6. Backend guarda estos IDs en la base de datos
7. Estado inicial: `processing`

#### 4. **Flujo de Reproducción**

**Endpoint: GET /videos/{id}/play**

1. Usuario solicita reproducir video
2. Backend consulta status actual a Mux
3. Si status = `ready`:
   - Genera URL de playback: `https://stream.mux.com/{playback_id}.m3u8`
   - Retorna URL al frontend
4. Si status = `processing`:
   - Retorna status, usuario debe esperar
5. Frontend usa HLS.js para reproducir el `.m3u8`

### Conexión con el Frontend

**Código en web/index.html:**

```javascript
async function playVideo(id, token) {
    const res = await fetch(`${apiBase}/videos/${id}/play`, {
        headers: { Authorization: `Bearer ${token}` }
    });
    const data = await res.json();
    
    if (data.status === 'ready') {
        const url = data.playback_url; // URL .m3u8
        hls = new Hls();               // HLS.js player
        hls.loadSource(url);           // Carga playlist
        hls.attachMedia(player);       // Adjunta a <video>
    }
}
```

**¿Qué es HLS (HTTP Live Streaming)?**

1. Video se divide en pequeños chunks (ej: 10 seg cada uno)
2. Archivo `.m3u8` lista todos los chunks y resoluciones
3. Player descarga chunks según sea necesario
4. Permite streaming adaptativo (cambia calidad en tiempo real)

---

## 🏗️ Arquitectura y Flujo de Datos

### Arquitectura de 3 Capas

```
┌─────────────┐
│  Frontend   │  (HTML + JS)
│  web/*.html │
└──────┬──────┘
       │ HTTP/REST API
       │ (JSON)
┌──────▼──────┐
│   Backend   │  FastAPI
│   main.py   │
│   app/*     │
└──────┬──────┘
       │ SQLAlchemy
       │ (SQL Queries)
┌──────▼──────┐
│  Database   │  PostgreSQL
│  Supabase   │
└─────────────┘
       
       Backend también se comunica con:
┌─────────────┐
│     Mux     │  Video API
│  (Externo)  │
└─────────────┘
```

### Flujo Completo: Registro → Login → Ver Video

#### 1. **Registro de Usuario**

```
Frontend (login.html)
  │
  │ POST /auth/register
  │ { email, password, role }
  ▼
Backend (app/auth/router.py)
  │
  │ 1. Valida datos (Pydantic)
  │ 2. Verifica que email no exista
  │ 3. Hash de password (bcrypt)
  │ 4. Crea usuario en DB
  │ 5. Genera JWT token
  │
  │ Response: { access_token, user }
  ▼
Frontend
  │
  │ Guarda token en localStorage
  │ Redirige a index.html
```

#### 2. **Login**

```
Frontend (login.html)
  │
  │ POST /auth/login
  │ { email, password }
  ▼
Backend (app/auth/router.py)
  │
  │ 1. Busca usuario por email
  │ 2. Verifica password (bcrypt)
  │ 3. Genera JWT token
  │
  │ Response: { access_token, user }
  ▼
Frontend
  │
  │ Guarda token en localStorage
  │ Redirige a index.html
```

#### 3. **Ver Catálogo de Videos**

```
Frontend (index.html)
  │
  │ GET /videos
  │ Headers: { Authorization: Bearer <token> }
  ▼
Backend (app/videos/router.py)
  │
  │ 1. Valida JWT token (get_current_user)
  │ 2. Consulta videos según rol:
  │    - USER: solo videos no-premium, no-hidden
  │    - PREMIUM: videos no-hidden
  │    - ADMIN: todos los videos
  │
  │ Response: [ { id, title, thumbnail_url, ... }, ... ]
  ▼
Frontend
  │
  │ Renderiza cards de video
  │ Muestra thumbnails de Mux
```

#### 4. **Reproducir Video**

```
Frontend (index.html)
  │
  │ GET /videos/{id}/play
  │ Headers: { Authorization: Bearer <token> }
  ▼
Backend (app/videos/router.py)
  │
  │ 1. Valida token y permisos
  │ 2. Consulta status a Mux API
  │ 3. Si ready, genera playback_url
  │
  │ Response: { status: "ready", playback_url }
  ▼
Frontend
  │
  │ HLS.js carga el .m3u8
  │ Descarga chunks de Mux CDN
  │ Reproduce video
```

### Sistema de Autenticación (JWT)

**¿Qué es JWT?**

JSON Web Token - un token autofirmado que contiene:
- `sub`: User ID
- `role`: Rol del usuario
- `exp`: Expiración (6 horas por defecto)

**Flujo de Autenticación:**

1. Usuario hace login
2. Backend crea JWT con `jose.jwt.encode()`
3. Frontend guarda token en `localStorage`
4. En cada request, frontend envía: `Authorization: Bearer <token>`
5. Backend valida token con `jose.jwt.decode()`
6. Si válido, extrae user_id y carga usuario desde DB

**Ventajas:**
- Stateless: no se guarda sesión en el servidor
- Escalable: cualquier instancia puede validar el token
- Seguro: firma criptográfica previene manipulación

---

## 📄 Descripción de Cada Archivo

### Raíz del Proyecto

#### **main.py**
**Propósito:** Punto de entrada de la aplicación FastAPI

**Funcionalidades:**
- Crea la instancia de FastAPI
- Configura CORS (permite requests desde cualquier origen)
- Crea tablas en la DB si no existen
- Registra routers (auth, admin, videos)
- Define endpoint de health check
- Sirve archivos estáticos del frontend

**Código clave:**
```python
app = FastAPI(title="Horios OTT", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"])
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(videos_router)
```

#### **requirements.txt**
**Propósito:** Lista todas las dependencias de Python

**Uso:**
```bash
pip install -r requirements.txt
```

#### **.env.example**
**Propósito:** Plantilla para variables de entorno

**El usuario debe copiar a `.env` y rellenar con sus credenciales:**
- `DATABASE_URL`: Conexión a PostgreSQL
- `JWT_SECRET`: Clave secreta para firmar tokens
- `MUX_TOKEN_ID` y `MUX_TOKEN_SECRET`: Credenciales de Mux

#### **README.md**
**Propósito:** Documentación básica del proyecto

Incluye:
- Instrucciones de setup
- Estructura del proyecto
- Tecnologías utilizadas
- Cómo correr el servidor

---

### Módulo: app/auth/ (Autenticación)

#### **router.py**
**Propósito:** Define endpoints de autenticación

**Endpoints:**
- `POST /auth/register`: Crear cuenta nueva
  - Valida que email no exista
  - Hash de contraseña
  - Crea usuario en DB
  - Retorna token JWT

- `POST /auth/login`: Iniciar sesión
  - Verifica credenciales
  - Retorna token JWT

- `GET /auth/me`: Obtener perfil del usuario actual
  - Requiere token válido
  - Retorna datos del usuario

#### **security.py**
**Propósito:** Funciones de seguridad

**Funciones:**
- `hash_password()`: Convierte password en hash bcrypt
- `verify_password()`: Compara password con hash
- `create_access_token()`: Genera JWT
- `decode_access_token()`: Decodifica y valida JWT

**Ejemplo:**
```python
hashed = hash_password("mi_password")  # $2b$12$xyz...
is_valid = verify_password("mi_password", hashed)  # True
token = create_access_token(subject="123", role="USER")
```

#### **deps.py**
**Propósito:** Dependencias reutilizables para endpoints

**Funciones:**
- `get_current_user()`: Extrae y valida token, retorna usuario
  - Usado como `Depends(get_current_user)` en endpoints
  - Si token inválido, lanza HTTPException 401

- `require_roles()`: Factory que crea guard de roles
  - Ejemplo: `Depends(require_roles(UserRole.ADMIN))`
  - Verifica que el usuario tenga uno de los roles permitidos

#### **schemas.py**
**Propósito:** Modelos Pydantic para validación de requests/responses

**Schemas:**
- `RegisterRequest`: email, password, role
- `LoginRequest`: email, password
- `AuthResponse`: access_token, user
- `UserResponse`: id, email, role, created_at

---

### Módulo: app/admin/ (Administración)

#### **router.py**
**Propósito:** Endpoints para gestión de usuarios (solo ADMIN)

**Endpoints:**
- `GET /admin/users`: Lista todos los usuarios
  - Solo accesible por ADMIN
  - Retorna lista completa de usuarios

- `PATCH /admin/users/{id}/role`: Cambiar rol de un usuario
  - Solo accesible por ADMIN
  - No puede degradar su propio rol de admin

#### **schemas.py**
**Propósito:** Modelos para administración

**Schemas:**
- `RoleUpdateRequest`: { role: "USER" | "PREMIUM" | "ADMIN" }

---

### Módulo: app/videos/ (Gestión de Videos)

#### **router.py**
**Propósito:** CRUD de videos y reproducción

**Endpoints:**
- `POST /videos`: Crear nuevo video (solo ADMIN)
  - Recibe `input_url` del video original
  - Llama a Mux para procesar
  - Guarda en DB con status "processing"

- `GET /videos`: Listar videos
  - Filtra según rol del usuario
  - USER: solo no-premium, no-hidden
  - PREMIUM: solo no-hidden
  - ADMIN: todos

- `GET /videos/{id}`: Obtener detalle de un video
  - Valida permisos según rol

- `GET /videos/{id}/play`: Obtener URL de reproducción
  - Consulta status actual a Mux
  - Si ready, retorna `playback_url`
  - Valida permisos de acceso

#### **schemas.py**
**Propósito:** Modelos de videos

**Schemas:**
- `VideoCreateRequest`: title, description, input_url, is_premium, is_hidden
- `VideoResponse`: Datos completos del video + thumbnail_url
- `PlayResponse`: status, playback_url

---

### Módulo: app/mux/ (Integración con Mux)

#### **service.py**
**Propósito:** Cliente para interactuar con la API de Mux

**Clase MuxService:**
- `create_asset()`: Crea un nuevo video asset en Mux
  - Envía URL del video original
  - Mux descarga y procesa
  - Retorna `mux_asset_id` y `playback_id`

- `get_asset_status()`: Consulta el estado del procesamiento
  - `processing`, `ready`, o `failed`

- `get_public_playback_url()`: Genera URL de streaming HLS
  - Formato: `https://stream.mux.com/{playback_id}.m3u8`

**Autenticación:**
```python
self.auth = (settings.mux_token_id, settings.mux_token_secret)
```
Usa HTTP Basic Auth con las credenciales de Mux.

---

### Módulo: app/db/ (Base de Datos)

#### **database.py**
**Propósito:** Configuración de la conexión a PostgreSQL

**Componentes:**
- `engine`: Motor de SQLAlchemy para conectar a PostgreSQL
- `SessionLocal`: Factory para crear sesiones
- `Base`: Clase base para modelos ORM
- `get_db()`: Generador que proporciona sesión y la cierra automáticamente

#### **models.py**
**Propósito:** Define modelos ORM (tablas de la base de datos)

**Modelo User:**
```python
class User(Base):
    __tablename__ = "users"
    id, email, password_hash, role, created_at
    videos = relationship("Video")  # Relación 1:N con Video
```

**Modelo Video:**
```python
class Video(Base):
    __tablename__ = "videos"
    id, title, description, is_premium, is_hidden
    mux_asset_id, playback_id, status
    created_by, created_at
    creator = relationship("User")  # Relación N:1 con User
```

**Enums:**
- `UserRole`: ADMIN, USER, PREMIUM
- `VideoStatus`: processing, ready, failed

---

### Módulo: app/core/ (Configuración)

#### **config.py**
**Propósito:** Centraliza la configuración de la aplicación

**Clase Settings:**
```python
class Settings(BaseSettings):
    database_url: str
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 360
    mux_token_id: str
    mux_token_secret: str
    api_base_url: str = "http://localhost:8000"
```

- Usa `pydantic-settings` para cargar desde `.env`
- Valida tipos automáticamente
- Valores por defecto para algunas variables

**Uso:**
```python
from app.core.config import settings
print(settings.database_url)
```

---

### Frontend: web/

#### **index.html**
**Propósito:** Página principal - catálogo y reproductor de videos

**Funcionalidades:**
- Muestra catálogo de videos (thumbnails)
- Reproductor de video con HLS.js
- Panel de admin (si el usuario es ADMIN)
  - Lista usuarios
  - Cambia roles de usuarios
- Autenticación:
  - Guarda token en `localStorage`
  - Envía token en cada request
  - Botón de logout

**APIs utilizadas:**
- `GET /auth/me`: Verificar sesión
- `GET /videos`: Listar videos
- `GET /videos/{id}/play`: Obtener URL de reproducción
- `GET /admin/users`: Listar usuarios (admin)
- `PATCH /admin/users/{id}/role`: Cambiar rol (admin)

**Tecnologías:**
- Vanilla JavaScript (sin frameworks)
- HLS.js para reproducción de video HLS
- CSS custom con gradientes y animaciones
- Fetch API para llamadas HTTP

#### **login.html**
**Propósito:** Página de login y registro

**Funcionalidades:**
- Formulario de login
- Formulario de registro
  - Selección de rol (USER o PREMIUM)
  - No permite registrarse como ADMIN
- Al recibir token, lo guarda y redirige a `index.html`

**APIs utilizadas:**
- `POST /auth/login`
- `POST /auth/register`

---

### Migraciones: migrations/

#### **001_initial_schema.sql**
**Propósito:** Crea el schema inicial de la base de datos

**Tablas creadas:**
- `users`: id, email, password_hash, role, created_at
- `videos`: id, title, description, is_premium, mux_asset_id, playback_id, status, created_by, created_at

**Índices creados:**
- `idx_users_email`: Para búsquedas por email
- `idx_videos_mux_asset_id`: Para consultas por asset de Mux
- `idx_videos_playback_id`: Para consultas por playback ID
- `idx_videos_created_by`: Para consultas por creador
- `idx_videos_status`: Para filtros por estado

#### **002_add_is_hidden.sql**
**Propósito:** Añade campo `is_hidden` a la tabla videos

Permite ocultar videos (solo visible para ADMIN).

---

### Scripts y Utilidades

#### **run_migrations.sh**
**Propósito:** Ejecuta todas las migraciones SQL en orden

**Uso:**
```bash
./run_migrations.sh
```

#### **setup.bat**
**Propósito:** Script de setup automático para Windows

#### **Horios_OTT.postman_collection.json**
**Propósito:** Colección de Postman para testing de la API

Incluye requests de ejemplo para todos los endpoints.

---

## 🔄 Flujo de Datos Detallado

### Ejemplo: Admin Sube un Video

1. **Admin hace login**
   - Frontend envía credenciales a `POST /auth/login`
   - Backend valida y retorna JWT token
   - Frontend guarda token en `localStorage`

2. **Admin accede al panel de admin** (hipotético - no implementado en UI)
   - Frontend envía `POST /videos` con:
     ```json
     {
       "title": "Mi Película",
       "description": "Una gran película",
       "input_url": "https://storage.example.com/video.mp4",
       "is_premium": true,
       "is_hidden": false
     }
     ```
   - Headers: `Authorization: Bearer <token>`

3. **Backend procesa la request**
   - `require_roles(UserRole.ADMIN)` valida que sea ADMIN
   - `MuxService.create_asset(input_url)` llama a Mux API
   - Mux recibe la URL y comienza a descargar/procesar
   - Mux retorna: `mux_asset_id="abc123"`, `playback_id="xyz789"`

4. **Backend guarda en DB**
   ```python
   video = Video(
       title="Mi Película",
       description="Una gran película",
       is_premium=True,
       is_hidden=False,
       mux_asset_id="abc123",
       playback_id="xyz789",
       status="processing",
       created_by=admin_user.id
   )
   db.add(video)
   db.commit()
   ```

5. **Frontend recibe respuesta**
   ```json
   {
     "id": 1,
     "title": "Mi Película",
     "status": "processing",
     "thumbnail_url": "https://image.mux.com/xyz789/thumbnail.jpg",
     ...
   }
   ```

6. **Mux procesa el video** (asíncrono, puede tardar minutos)
   - Descarga el video desde `input_url`
   - Lo transcode a múltiples resoluciones
   - Genera chunks HLS
   - Actualiza status a `ready`

7. **Usuario intenta reproducir**
   - Frontend: `GET /videos/1/play`
   - Backend: Consulta a Mux el status actual
   - Si `ready`: Retorna `playback_url`
   - Frontend: HLS.js reproduce el video

---

## 🔐 Seguridad

### Medidas de Seguridad Implementadas

1. **Hash de Contraseñas**
   - Bcrypt con cost factor automático
   - Nunca se almacenan contraseñas en texto plano

2. **JWT Tokens**
   - Tokens firmados criptográficamente
   - Expiración de 6 horas
   - No se pueden falsificar sin la secret key

3. **Control de Acceso Basado en Roles (RBAC)**
   - USER: Solo contenido gratuito
   - PREMIUM: Todo contenido no-oculto
   - ADMIN: Control total

4. **Validación de Datos**
   - Pydantic valida todos los inputs
   - Previene inyección de datos maliciosos

5. **CORS Configurado**
   - Aunque actualmente permite `*`, en producción debe restringirse

6. **SQL Injection Prevention**
   - SQLAlchemy ORM usa parametrización automática
   - No se ejecuta SQL raw directamente

7. **Protección de Endpoints**
   - Todos los endpoints requieren autenticación (excepto login/register)
   - Endpoints de admin verifican rol

### Mejoras de Seguridad Recomendadas

1. **HTTPS en Producción**
   - Los tokens JWT deben transmitirse solo via HTTPS

2. **Rate Limiting**
   - Prevenir ataques de fuerza bruta en login

3. **Refresh Tokens**
   - Tokens de corta duración + refresh tokens

4. **CORS Restrictivo**
   - Solo permitir orígenes confiables

5. **Validación de Input URLs**
   - Validar `input_url` para prevenir SSRF

---

## 📊 Casos de Uso

### Caso de Uso 1: Usuario Gratuito Ve Contenido

1. Usuario se registra con rol USER
2. Ve catálogo - solo videos gratuitos
3. Intenta ver video premium - recibe error 403
4. Reproduce video gratuito exitosamente

### Caso de Uso 2: Usuario Premium

1. Usuario paga y se le actualiza rol a PREMIUM
2. Ve catálogo - todos los videos (excepto ocultos)
3. Reproduce cualquier video premium
4. Disfruta de contenido exclusivo

### Caso de Uso 3: Admin Gestiona Plataforma

1. Admin hace login
2. Sube nuevo video proporcionando URL
3. Mux procesa el video
4. Admin marca video como premium u oculto
5. Admin cambia roles de usuarios (ej: USER → PREMIUM)
6. Admin ve todos los videos, incluidos ocultos

---

## 🚀 Cómo Ejecutar el Proyecto

### 1. Clonar el repositorio
```bash
git clone <repo-url>
cd Horios-OTT
```

### 2. Crear entorno virtual
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
```bash
cp .env.example .env
# Editar .env con tus credenciales
```

### 5. Ejecutar migraciones
```bash
./run_migrations.sh  # Linux/Mac
# O ejecutar manualmente cada .sql en la DB
```

### 6. Iniciar servidor
```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 7. Acceder a la aplicación
- Frontend: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Login: http://localhost:8000/login

---

## 📚 Recursos Adicionales

### Documentación de Tecnologías

- **FastAPI**: https://fastapi.tiangolo.com/
- **SQLAlchemy**: https://docs.sqlalchemy.org/
- **Pydantic**: https://docs.pydantic.dev/
- **Mux Video API**: https://docs.mux.com/
- **HLS.js**: https://github.com/video-dev/hls.js/
- **JWT**: https://jwt.io/

### Conceptos Clave para Estudiar

1. **RESTful APIs**: Diseño de APIs HTTP
2. **ORM (Object-Relational Mapping)**: Mapeo de objetos a tablas
3. **JWT (JSON Web Tokens)**: Autenticación stateless
4. **HLS (HTTP Live Streaming)**: Streaming adaptativo
5. **CDN (Content Delivery Network)**: Distribución global de contenido
6. **Async/Await**: Programación asíncrona en Python
7. **Dependency Injection**: Patrón de diseño en FastAPI
8. **CORS (Cross-Origin Resource Sharing)**: Seguridad en APIs web

---

## 🎓 Conclusión

Este proyecto es una excelente introducción a:
- Desarrollo backend moderno con Python y FastAPI
- Arquitectura de microservicios (Backend + Mux)
- Integración con APIs externas (Mux)
- Autenticación y autorización (JWT + RBAC)
- Streaming de video con tecnologías modernas (HLS)
- ORMs y gestión de bases de datos
- Desarrollo full-stack (Backend + Frontend básico)

**Horios OTT** demuestra cómo construir una plataforma de streaming escalable y profesional con herramientas modernas, delegando la complejidad del video a servicios especializados como Mux.
