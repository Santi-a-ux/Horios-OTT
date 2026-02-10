-- Migration: Create users and videos tables
-- Date: 2026-02-07

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'USER' CHECK (role IN ('ADMIN', 'USER', 'PREMIUM')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE INDEX idx_users_email ON users(email);

CREATE TABLE IF NOT EXISTS videos (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    is_premium BOOLEAN DEFAULT FALSE NOT NULL,
    mux_asset_id VARCHAR(255),
    playback_id VARCHAR(255),
    status VARCHAR(50) NOT NULL DEFAULT 'processing' CHECK (status IN ('processing', 'ready', 'failed')),
    created_by INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE INDEX idx_videos_mux_asset_id ON videos(mux_asset_id);
CREATE INDEX idx_videos_playback_id ON videos(playback_id);
CREATE INDEX idx_videos_created_by ON videos(created_by);
CREATE INDEX idx_videos_status ON videos(status);
