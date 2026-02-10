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
# Database - Supabase (pooler)
DATABASE_URL=postgresql://postgres.whjovldnkmxkmtsrncop:I7KJlgIGvTYviZIY@aws-0-us-west-2.pooler.supabase.com:5432/postgres

# JWT - Genera una secret segura en producción
JWT_SECRET=your-super-secret-key-min-32-chars-here-change-me
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=360

# Mux - Credentials
MUX_TOKEN_ID=1bcd0f5a-78a2-4944-90e3-d6a8a70fbd38
MUX_TOKEN_SECRET=tuPowCfY1RbmqfFSq/loFXGR7a7fire+IKNyiVP2T+rrNMjowVFpf/4nh4qDQuS/nNdTjmA/1oH

# API
API_BASE_URL=http://localhost:8000

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
