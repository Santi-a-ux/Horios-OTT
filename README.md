# Horios OTT - Backend

OTT (Over-The-Top) streaming platform con FastAPI, PostgreSQL y Mux.

## Setup Rápido

### 1. Variables de entorno
```bash
cp .env.example .env
# Edita .env con tus credenciales
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Crear tablas en Postgres
Ejecuta el SQL en `migrations/001_initial_schema.sql` en tu DB (Supabase, Neon, etc)

O usa:
```bash
./run_migrations.sh  # Linux/Mac
psql $DATABASE_URL -f migrations/001_initial_schema.sql  # Windows
```

### 4. Correr servidor
```bash
uvicorn main:app --reload
```

Visita: http://localhost:8000/docs

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
