from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pathlib import Path
from app.db.database import Base, engine
from app.db.models import User, Video
from app.auth.router import router as auth_router
from app.admin.router import router as admin_router
from app.videos.router import router as videos_router

# Create app
app = FastAPI(title="Horios OTT", version="0.1.0")

# Create tables (lazy - only if needed)
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"⚠️  DB connection failed: {e}")
    print("⚠️  Running in API-only mode (no persistence)")
    print("    Connect DATABASE_URL when ready")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(videos_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}


# Placeholder routes (se llenan en siguientes días)
@app.get("/")
def root():
    web_path = Path(__file__).parent / "web" / "index.html"
    if web_path.exists():
        return FileResponse(web_path)
    return {"message": "Horios OTT API"}


@app.get("/login")
def login_page():
    web_path = Path(__file__).parent / "web" / "login.html"
    if web_path.exists():
        return FileResponse(web_path)
    return {"message": "Login page not found"}
