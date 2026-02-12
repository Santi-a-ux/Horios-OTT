# Análisis Tecnológico del Proyecto Horios OTT

## Resumen Ejecutivo

**Horios OTT** es una plataforma de streaming de video Over-The-Top (OTT) construida con tecnologías modernas de Python y servicios en la nube. El proyecto implementa un sistema completo de gestión de videos con autenticación de usuarios, control de acceso basado en roles, y procesamiento de video mediante Mux.

---

## 1. Tecnologías Utilizadas

### 1.1 Backend Framework

#### **FastAPI (v0.104.1)**
- **Uso**: Framework web principal para construir la API REST
- **Por qué se usó**: 
  - Alto rendimiento comparable a NodeJS y Go
  - Validación automática de datos con Pydantic
  - Documentación interactiva automática (Swagger/OpenAPI)
  - Soporte nativo para async/await
  - Type hints de Python para mejor desarrollo

**Implementación en el proyecto:**
```python
# main.py
app = FastAPI(title="Horios OTT", version="0.1.0")
```

El servidor se ejecuta con **Uvicorn (v0.24.0)**, un servidor ASGI de alto rendimiento que soporta las capacidades asíncronas de FastAPI.

---

### 1.2 Base de Datos

#### **PostgreSQL con SQLAlchemy (v2.0.23)**

**PostgreSQL**:
- **Uso**: Base de datos relacional principal
- **Por qué se usó**:
  - Base de datos robusta y confiable para producción
  - Soporte completo de ACID (transacciones)
  - Excelente para datos estructurados (usuarios, videos)
  - Compatible con Supabase y Neon para hosting cloud

**SQLAlchemy**:
- **Uso**: ORM (Object-Relational Mapping) para interactuar con la base de datos
- **Por qué se usó**:
  - Abstracción de alto nivel sobre SQL
  - Prevención de SQL injection
  - Migraciones y versionado de esquemas
  - Relaciones entre modelos fáciles de manejar

**Estructura de la Conexión a Base de Datos:**

```python
# app/db/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 1. Crear el engine - conexión principal a PostgreSQL
engine = create_engine(
    settings.database_url,  # PostgreSQL connection string
    echo=False,              # No mostrar SQL en logs
    pool_pre_ping=True,      # Verificar conexiones antes de usar
)

# 2. SessionLocal - factory para crear sesiones de BD
SessionLocal = sessionmaker(
    autocommit=False,  # Transacciones manuales
    autoflush=False,   # Control manual de flush
    bind=engine        # Vincular al engine
)

# 3. Dependency injection para endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db  # Proporcionar sesión al endpoint
    finally:
        db.close()  # Siempre cerrar la conexión
```

**Uso en endpoints:**
```python
@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    # ... lógica de autenticación
```

**Modelos de Datos:**

El proyecto define dos modelos principales:

1. **User** (`app/db/models.py`):
   - id: Identificador único
   - email: Email único del usuario
   - password_hash: Contraseña hasheada (nunca en texto plano)
   - role: ADMIN, USER, o PREMIUM
   - created_at: Fecha de creación

2. **Video** (`app/db/models.py`):
   - id: Identificador único
   - title: Título del video
   - description: Descripción
   - is_premium: Indica si es contenido premium
   - is_hidden: Indica si está oculto
   - mux_asset_id: ID del asset en Mux
   - playback_id: ID de reproducción de Mux
   - status: processing, ready, o failed
   - created_by: Relación con el usuario creador

**Migraciones SQL:**

El proyecto incluye migraciones manuales en la carpeta `migrations/`:
- `001_initial_schema.sql`: Crea tablas users y videos con índices
- `002_add_is_hidden.sql`: Agrega columna is_hidden a videos

**Conector PostgreSQL:**
- **psycopg2-binary (v2.9.9)**: Driver de PostgreSQL para Python

---

### 1.3 Autenticación y Seguridad

#### **JWT (JSON Web Tokens) con python-jose (v3.3.0)**

- **Uso**: Autenticación stateless basada en tokens
- **Por qué se usó**:
  - No requiere almacenar sesiones en el servidor
  - Escalable para APIs distribuidas
  - Incluye claims como rol y expiración
  - Estándar de la industria

**Implementación:**
```python
# app/auth/security.py
def create_access_token(subject: str, role: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=360)
    to_encode = {
        "sub": subject,  # user_id
        "role": role,    # ADMIN, USER, PREMIUM
        "exp": expire    # Expiración
    }
    return jwt.encode(to_encode, settings.jwt_secret, algorithm="HS256")
```

**Flujo de autenticación:**
1. Usuario envía credenciales a `/auth/login`
2. Backend verifica password con bcrypt
3. Se genera JWT con user_id y role
4. Cliente incluye JWT en header `Authorization: Bearer <token>`
5. Middleware `get_current_user` valida token en cada request

#### **bcrypt (v3.2.2) con passlib (v1.7.4)**

- **Uso**: Hashing seguro de contraseñas
- **Por qué se usó**:
  - Algoritmo de hashing lento (resistente a fuerza bruta)
  - Salt automático (previene rainbow tables)
  - Estándar de seguridad en la industria

```python
# app/auth/security.py
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)  # Genera hash + salt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
```

#### **OAuth2PasswordBearer**

- **Uso**: Esquema de autenticación para FastAPI
- **Por qué se usó**: Integración automática con Swagger UI para testing

---

### 1.4 Validación de Datos

#### **Pydantic (v2.5.0)**

- **Uso**: Validación automática de datos de entrada/salida
- **Por qué se usó**:
  - Validación en tiempo de ejecución con type hints
  - Serialización/deserialización automática
  - Mensajes de error claros
  - Integración nativa con FastAPI

**Ejemplo de schemas:**
```python
# app/auth/schemas.py
class RegisterRequest(BaseModel):
    email: EmailStr  # Valida formato de email
    password: str    # Campo requerido
    role: UserRole = UserRole.USER  # Default value

class AuthResponse(BaseModel):
    access_token: str
    user: UserResponse
```

**pydantic-settings (v2.1.0)**: Para cargar configuración desde variables de entorno

---

### 1.5 Integración de Video - Mux

#### **Mux Video API con mux-python (v5.1.2)**

**¿Qué es Mux?**
Mux es una plataforma de video en la nube que proporciona:
- Codificación de video (transcoding)
- Almacenamiento de videos
- Streaming adaptativo (HLS)
- CDN global
- Thumbnails automáticos
- Analytics de reproducción

**¿Por qué se usó Mux?**
- Evita construir infraestructura propia de video
- Transcoding automático a múltiples resoluciones
- Streaming optimizado con HLS (HTTP Live Streaming)
- Entrega global mediante CDN
- Generación automática de thumbnails
- No requiere gestión de servidores de video

**Conexión a Mux:**

```python
# app/mux/service.py
class MuxService:
    def __init__(self):
        self.base_url = "https://api.mux.com/video/v1"
        # Autenticación con HTTP Basic Auth
        self.auth = (settings.mux_token_id, settings.mux_token_secret)
```

**Credenciales requeridas** (en `.env`):
- `MUX_TOKEN_ID`: Token de acceso de Mux
- `MUX_TOKEN_SECRET`: Secret del token

**Flujos de trabajo con Mux:**

1. **Crear Asset (Subir Video):**
```python
def create_asset(self, input_url: str) -> Tuple[str, str]:
    payload = {
        "input": [{"url": input_url}],  # URL del video original
        "playback_policy": ["public"],  # Acceso público
    }
    response = requests.post(
        f"{self.base_url}/assets",
        json=payload,
        auth=self.auth,  # HTTP Basic Auth
    )
    data = response.json()["data"]
    return data["id"], data["playback_ids"][0]["id"]
```

**¿Qué hace este método?**
- Envía URL del video a Mux
- Mux descarga, procesa y codifica el video
- Retorna `mux_asset_id` (identificador interno) y `playback_id` (para streaming)

2. **Verificar Estado del Video:**
```python
def get_asset_status(self, mux_asset_id: str) -> str:
    response = requests.get(
        f"{self.base_url}/assets/{mux_asset_id}",
        auth=self.auth,
    )
    data = response.json()["data"]
    return data.get("status", "processing")
```

Estados posibles:
- `processing`: Mux está codificando el video
- `ready`: Video listo para streaming
- `failed`: Error en el procesamiento

3. **Generar URL de Reproducción:**
```python
@staticmethod
def get_public_playback_url(playback_id: str) -> str:
    return f"https://stream.mux.com/{playback_id}.m3u8"
```

**Formato HLS (.m3u8):**
- HTTP Live Streaming de Apple
- Streaming adaptativo (ajusta calidad según bandwidth)
- Compatible con todos los navegadores modernos
- Reproducible con hls.js en el frontend

4. **Generar Thumbnail:**
```python
# app/videos/router.py
thumbnail_url = f"https://image.mux.com/{playback_id}/thumbnail.jpg?time=0"
```

**Finalidad de Mux en el proyecto:**
- **Almacenamiento**: Guarda videos de forma permanente
- **Transcoding**: Convierte videos a múltiples formatos/resoluciones
- **Streaming**: CDN global para entrega rápida
- **Adaptabilidad**: Ajusta calidad según conexión del usuario
- **Thumbnails**: Genera previsualizaciones automáticas
- **Sin infraestructura**: No requiere gestionar servidores propios

**Integración con la base de datos:**
```python
# Al crear video
video = Video(
    title="Mi Video",
    mux_asset_id="abc123",      # ID de Mux
    playback_id="xyz789",        # ID para streaming
    status="processing",         # Estado inicial
)
```

---

### 1.6 HTTP Client

#### **requests (v2.31.0)**

- **Uso**: Cliente HTTP para llamadas a API externa de Mux
- **Por qué se usó**: Biblioteca estándar de Python para HTTP requests

---

### 1.7 Middleware y Utilidades

#### **CORS Middleware**

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Permite todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],      # Permite todos los métodos HTTP
    allow_headers=["*"],      # Permite todos los headers
)
```

- **Uso**: Permitir requests desde frontend en diferentes dominios
- **Por qué se usó**: SPA (Single Page Application) necesita CORS

#### **python-multipart (v0.0.6)**

- **Uso**: Parseo de formularios multipart (file uploads)
- **Por qué se usó**: Soporte para subida de archivos en FastAPI

#### **python-dotenv (v1.0.0)**

- **Uso**: Cargar variables de entorno desde archivo `.env`
- **Por qué se usó**: Gestión segura de configuración sensible

---

### 1.8 Migraciones

#### **Alembic (v1.13.0)**

- **Uso**: Sistema de migraciones de base de datos
- **Por qué se usó**: Versionado y control de cambios en el esquema

**Actualmente**: El proyecto usa migraciones SQL manuales en `migrations/`, pero Alembic está disponible para futuras migraciones automáticas.

---

## 2. Arquitectura de Base de Datos

### 2.1 Configuración de Conexión

**Variables de entorno requeridas:**
```bash
DATABASE_URL=postgresql://user:password@host:5432/database?sslmode=require
```

**Formato de URL:**
- `postgresql://`: Protocolo PostgreSQL
- `user:password`: Credenciales
- `host:5432`: Servidor y puerto
- `/database`: Nombre de la base de datos
- `?sslmode=require`: Conexión SSL obligatoria (seguridad)

**Proveedor recomendado**: Supabase o Neon (PostgreSQL cloud)

### 2.2 Pool de Conexiones

```python
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,  # Verifica conexiones antes de usar
)
```

`pool_pre_ping=True` asegura que conexiones obsoletas se reciclen automáticamente.

### 2.3 Gestión de Sesiones

**Patrón de Dependency Injection:**
```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

Este patrón garantiza:
- Una sesión por request
- Cierre automático de conexión
- Manejo de errores sin dejar conexiones abiertas

### 2.4 Tablas y Relaciones

**Diagrama de relaciones:**
```
users (1) ──── (N) videos
   │
   └─ Un usuario puede crear múltiples videos
```

**Índices creados:**
- `users.email`: Búsqueda rápida por email
- `videos.mux_asset_id`: Búsqueda por asset de Mux
- `videos.playback_id`: Búsqueda por playback ID
- `videos.created_by`: Join con users
- `videos.status`: Filtrado por estado

---

## 3. Sistema de Control de Acceso

### 3.1 Roles de Usuario

```python
class UserRole(str, enum.Enum):
    ADMIN = "ADMIN"      # Acceso total
    PREMIUM = "PREMIUM"  # Acceso a contenido premium
    USER = "USER"        # Acceso a contenido gratuito
```

### 3.2 Lógica de Permisos

**Videos:**
- `USER`: Solo videos no-premium y no-hidden
- `PREMIUM`: Todos los videos no-hidden
- `ADMIN`: Todos los videos (incluyendo hidden)

**Endpoints protegidos:**
```python
@router.post("/videos")
def create_video(
    current_user: User = Depends(require_roles(UserRole.ADMIN))
):
    # Solo admins pueden crear videos
```

### 3.3 Flujo de Autenticación

1. **Registro** (`POST /auth/register`):
   - Valida email único
   - Hashea password con bcrypt
   - Crea usuario con rol USER o PREMIUM
   - Retorna JWT

2. **Login** (`POST /auth/login`):
   - Verifica credenciales
   - Genera JWT con user_id y role
   - Retorna token + datos de usuario

3. **Acceso a Recursos**:
   - Cliente envía JWT en header
   - Middleware valida token
   - Extrae user_id y carga usuario desde BD
   - Verifica permisos según rol

---

## 4. Flujo Completo de Video

### 4.1 Crear Video (Admin)

```
1. POST /videos
   ├─ Input: title, description, is_premium, input_url
   ├─ Autenticación: JWT (ADMIN)
   │
2. MuxService.create_asset(input_url)
   ├─ Envía video a Mux API
   ├─ Mux procesa video
   └─ Retorna: mux_asset_id, playback_id
   │
3. Guardar en BD
   ├─ Crear registro Video
   ├─ status = "processing"
   └─ Commit
   │
4. Retornar VideoResponse
   └─ Incluye thumbnail_url automático
```

### 4.2 Listar Videos (Usuario)

```
1. GET /videos
   ├─ Autenticación: JWT
   │
2. Filtrar según rol
   ├─ USER: is_premium=false, is_hidden=false
   ├─ PREMIUM: is_hidden=false
   └─ ADMIN: todos
   │
3. Retornar lista con thumbnails
```

### 4.3 Reproducir Video

```
1. GET /videos/{id}/play
   ├─ Autenticación: JWT
   │
2. Verificar permisos
   ├─ Usuario tiene acceso según rol?
   └─ Video no está hidden?
   │
3. Actualizar estado desde Mux
   ├─ MuxService.get_asset_status()
   └─ Actualizar BD si cambió
   │
4. Si status = "ready"
   ├─ Generar playback_url (HLS)
   └─ Retornar URL para streaming
   │
5. Frontend reproduce con hls.js
   └─ Streaming adaptativo desde CDN de Mux
```

---

## 5. Frontend Web

### 5.1 Tecnologías

**HTML + JavaScript Vanilla:**
- `web/index.html`: Página principal con galería de videos
- `web/login.html`: Página de login/registro

**Librerías:**
- **hls.js**: Reproducción de video HLS en navegador
- **Tailwind-like CSS**: Diseño moderno con variables CSS

### 5.2 Funcionalidades

- Autenticación con JWT
- Galería de videos con thumbnails
- Reproductor de video integrado
- Sistema de roles (premium/free)

---

## 6. Estructura del Proyecto

```
Horios-OTT/
├── app/
│   ├── auth/           # Autenticación y JWT
│   │   ├── router.py   # Endpoints: register, login, me
│   │   ├── security.py # Hashing y JWT
│   │   ├── deps.py     # Dependencias: get_current_user
│   │   └── schemas.py  # Pydantic models
│   │
│   ├── admin/          # Panel de administración
│   │   ├── router.py   # Endpoints: list_users, update_role
│   │   └── schemas.py
│   │
│   ├── videos/         # Gestión de videos
│   │   ├── router.py   # CRUD de videos + play
│   │   └── schemas.py
│   │
│   ├── mux/            # Integración con Mux
│   │   └── service.py  # MuxService: create_asset, get_status
│   │
│   ├── core/           # Configuración
│   │   └── config.py   # Settings con pydantic-settings
│   │
│   └── db/             # Base de datos
│       ├── database.py # Engine, SessionLocal, get_db
│       └── models.py   # User, Video models
│
├── migrations/         # Migraciones SQL
│   ├── 001_initial_schema.sql
│   └── 002_add_is_hidden.sql
│
├── web/                # Frontend
│   ├── index.html      # Página principal
│   └── login.html      # Login/registro
│
├── main.py             # Punto de entrada FastAPI
├── requirements.txt    # Dependencias Python
└── .env.example        # Variables de entorno template
```

---

## 7. Seguridad Implementada

### 7.1 Contraseñas
- ✅ Hashing con bcrypt (nunca texto plano)
- ✅ Salt automático por bcrypt
- ✅ Algoritmo lento (resistente a brute force)

### 7.2 Autenticación
- ✅ JWT con expiración (360 minutos)
- ✅ HS256 signing algorithm
- ✅ Secret key en variable de entorno

### 7.3 Base de Datos
- ✅ SQLAlchemy ORM (previene SQL injection)
- ✅ Conexión SSL (sslmode=require)
- ✅ Pool de conexiones con pre-ping

### 7.4 API
- ✅ CORS configurado
- ✅ Validación de datos con Pydantic
- ✅ Control de acceso basado en roles
- ✅ HTTP Basic Auth para Mux

---

## 8. Variables de Entorno Requeridas

```bash
# Base de Datos PostgreSQL
DATABASE_URL=postgresql://user:password@host:5432/database?sslmode=require

# JWT (cambiar en producción)
JWT_SECRET=your-super-secret-key-min-32-chars-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=360

# Mux Video Platform
MUX_TOKEN_ID=your-mux-token-id
MUX_TOKEN_SECRET=your-mux-token-secret

# API URL
API_BASE_URL=http://localhost:8000
```

---

## 9. Despliegue y Escalabilidad

### 9.1 Recomendaciones de Hosting

**Backend:**
- Railway, Render, o Fly.io
- Requerimientos: Python 3.10+, PostgreSQL

**Base de Datos:**
- Supabase (PostgreSQL managed)
- Neon (Serverless PostgreSQL)

**Videos:**
- Mux maneja todo el hosting y CDN

### 9.2 Ventajas de la Arquitectura

- **Stateless**: JWT permite escalado horizontal
- **Desacoplado**: Backend API + Frontend separados
- **Cloud-native**: Mux + PostgreSQL cloud
- **Sin servidores de video**: Mux maneja infraestructura

---

## 10. Conclusiones

**Horios OTT** es una plataforma moderna de streaming que:

1. **Utiliza FastAPI** para una API REST de alto rendimiento
2. **PostgreSQL + SQLAlchemy** para gestión de datos robusta
3. **JWT + bcrypt** para autenticación segura
4. **Mux** para toda la infraestructura de video (storage, transcoding, streaming)
5. **Control de acceso** por roles (ADMIN, PREMIUM, USER)
6. **Arquitectura cloud-native** lista para producción

**Decisiones clave:**
- Mux elimina complejidad de gestionar video infrastructure
- JWT permite escalado sin estado de sesión
- PostgreSQL cloud (Supabase/Neon) simplifica operaciones
- FastAPI + Pydantic garantizan validación y documentación automática

El proyecto está diseñado para ser **fácil de desplegar**, **escalable**, y **mantenible**, utilizando servicios cloud en lugar de infraestructura propia.
