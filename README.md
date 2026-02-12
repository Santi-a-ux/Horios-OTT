# Horios OTT - Backend

OTT (Over-The-Top) streaming platform con FastAPI, PostgreSQL y Mux.

## 📚 Documentación Completa

Para una guía de estudio detallada del proyecto, incluyendo explicaciones de todas las tecnologías, arquitectura, y el propósito de cada archivo, consulta:

**[GUIA_DE_ESTUDIO.md](GUIA_DE_ESTUDIO.md)** - Guía completa en español que cubre:
- Todas las tecnologías utilizadas y por qué
- Estructura completa del proyecto
- Explicación detallada de la integración con Mux
- Conexión con la base de datos PostgreSQL
- Arquitectura y flujos de datos
- Descripción de cada archivo y módulo
- Casos de uso y ejemplos prácticos

---

## Setup Rápido

### 1. Variables de entorno
```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```
### 3.
cp .env.example .env

### 4.
```bash
# Database - Supabase (pooler)
DATABASE_URL=postgresql://postgres.whjovldnkmxkmtsrncop:I7KJlgIGvTYviZIY@aws-0-us-west-2.pooler.supabase.com:6543/postgres?sslmode=require

# JWT - Genera una secret segura en producción
JWT_SECRET=your-super-secret-key-min-32-chars-here-change-me
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=360

# Mux - Credentials
MUX_TOKEN_ID=dbe54439-74e3-467e-9d4f-9516339196b6
MUX_TOKEN_SECRET=vHRqy+HV9fq3tMI0ZpIGPZCOKdAXC0B6GLweJttevLuCDgwMN5pOLW5h8N32uUaIdPlgoyH1wre
# API
API_BASE_URL=http://localhost:8000

```

### 5. Correr servidor
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

### 6. Visita: http://localhost:8000/docs

## Estructura

```
app/
  ├── auth/         # Autenticación (JWT, login, register)
  ├── users/        # Gestión de usuarios
  ├── videos/       # Gestión de videos
  ├── mux/          # Integración con Mux
  ├── core/         # Config, logging, permisos
  └── db/           # Models, database connection
migrations/         # SQL migrations
main.py            # FastAPI app
```

## Tecnología

- **Backend**: FastAPI
- **DB**: PostgreSQL (Supabase/Neon recomendado)
- **Video**: Mux
- **Auth**: JWT (python-jose)
- **Hash**: bcrypt
