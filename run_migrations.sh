#!/bin/bash

# Script para crear las tablas en Supabase/Postgres
# Uso: ./run_migrations.sh

DB_URL=${DATABASE_URL}

if [ -z "$DB_URL" ]; then
    echo "Error: DATABASE_URL no está configurada"
    exit 1
fi

echo "Ejecutando migraciones..."
psql "$DB_URL" -f migrations/001_initial_schema.sql

echo "✅ Migraciones completadas"
