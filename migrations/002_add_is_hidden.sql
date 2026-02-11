-- Migration: Add is_hidden to videos
-- Date: 2026-02-10

ALTER TABLE videos
ADD COLUMN IF NOT EXISTS is_hidden BOOLEAN DEFAULT FALSE NOT NULL;

CREATE INDEX IF NOT EXISTS idx_videos_is_hidden ON videos(is_hidden);
