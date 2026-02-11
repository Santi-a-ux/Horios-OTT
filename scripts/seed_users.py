import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models import User, UserRole
from app.auth.security import hash_password


def ensure_user(db: Session, email: str, password: str, role: UserRole) -> None:
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        existing.role = role
        existing.password_hash = hash_password(password)
        db.commit()
        return
    user = User(
        email=email,
        password_hash=hash_password(password),
        role=role,
    )
    db.add(user)
    db.commit()


def main() -> int:
    password = "password123"
    if "--password" in sys.argv:
        idx = sys.argv.index("--password")
        if idx + 1 < len(sys.argv):
            password = sys.argv[idx + 1]

    users_to_seed = [
        ("admin@example.com", "admin123", UserRole.ADMIN),
        ("pepito@example.com", "password123", UserRole.USER),
        ("juancito.premium@example.com", "password123", UserRole.PREMIUM),
    ]

    db = SessionLocal()
    try:
        for email, password, role in users_to_seed:
            ensure_user(db, email, password, role)
    finally:
        db.close()

    print("Seeded users: pepito@example.com, juancito.premium@example.com")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
