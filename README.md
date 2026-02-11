# Horios OTT - Backend

OTT (Over-The-Top) streaming platform con FastAPI, PostgreSQL y Mux.

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
DATABASE_URL=postgresql://postgres.<project-ref>:<password>@aws-0-us-west-2.pooler.supabase.com:6543/postgres?sslmode=require

# JWT - Genera una secret segura en produccion
JWT_SECRET=your-super-secret-key-min-32-chars-here-change-me
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=360

# Mux - Credentials
MUX_TOKEN_ID=your-mux-token-id
MUX_TOKEN_SECRET=your-mux-token-secret

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
