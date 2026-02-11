import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.db.database import SessionLocal
from app.db.models import Video


def main() -> int:
    db = SessionLocal()
    try:
        count = db.query(Video).delete()
        db.commit()
        print(f"Deleted videos: {count}")
        return 0
    finally:
        db.close()


if __name__ == "__main__":
    raise SystemExit(main())
