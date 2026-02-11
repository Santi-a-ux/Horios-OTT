import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models import Video, VideoStatus
from app.mux.service import MuxService

VIDEOS = [
    {
        "title": "Big Buck Bunny",
        "description": "Big Buck Bunny tells the story of a giant rabbit with a heart bigger than himself.",
        "url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
        "is_premium": False,
        "is_hidden": False,
    },
    {
        "title": "Elephant Dream",
        "description": "The first Blender Open Movie from 2006.",
        "url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4",
        "is_premium": False,
        "is_hidden": False,
    },
    {
        "title": "For Bigger Blazes",
        "description": "Chromecast demo by Google.",
        "url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
        "is_premium": True,
        "is_hidden": False,
    },
    {
        "title": "For Bigger Escape",
        "description": "Chromecast demo by Google.",
        "url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4",
        "is_premium": False,
        "is_hidden": False,
    },
    {
        "title": "For Bigger Fun",
        "description": "Chromecast demo by Google.",
        "url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4",
        "is_premium": True,
        "is_hidden": False,
    },
    {
        "title": "For Bigger Joyrides",
        "description": "Chromecast demo by Google.",
        "url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4",
        "is_premium": False,
        "is_hidden": False,
    },
    {
        "title": "For Bigger Meltdowns",
        "description": "Chromecast demo by Google.",
        "url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerMeltdowns.mp4",
        "is_premium": True,
        "is_hidden": False,
    },
    {
        "title": "Sintel",
        "description": "Open movie by Blender Foundation.",
        "url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/Sintel.mp4",
        "is_premium": True,
        "is_hidden": True,
    },
    {
        "title": "Subaru Outback On Street And Dirt",
        "description": "Garage419 demo.",
        "url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/SubaruOutbackOnStreetAndDirt.mp4",
        "is_premium": False,
        "is_hidden": False,
    },
    {
        "title": "Tears of Steel",
        "description": "Sci-fi film by Blender Foundation.",
        "url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/TearsOfSteel.mp4",
        "is_premium": True,
        "is_hidden": True,
    },
    # NOTE: Keep this list at 10 items for Mux free plan.
]


def ensure_video(db: Session, mux_service: MuxService, item: dict, created_by: int) -> str:
    existing = db.query(Video).filter(Video.title == item["title"]).first()
    if existing:
        existing.is_premium = item["is_premium"]
        existing.is_hidden = item["is_hidden"]
        db.commit()
        return "updated"

    mux_asset_id, playback_id = mux_service.create_asset(item["url"])
    video = Video(
        title=item["title"],
        description=item["description"],
        is_premium=item["is_premium"],
        is_hidden=item["is_hidden"],
        mux_asset_id=mux_asset_id,
        playback_id=playback_id,
        status=VideoStatus.PROCESSING.value,
        created_by=created_by,
    )
    db.add(video)
    db.commit()
    print(f"created asset: {mux_asset_id} | playback_id={playback_id}")
    return "created"


def main() -> int:
    created_by = 1
    if "--created-by" in sys.argv:
        idx = sys.argv.index("--created-by")
        if idx + 1 < len(sys.argv):
            created_by = int(sys.argv[idx + 1])

    db = SessionLocal()
    created = 0
    updated = 0
    try:
        mux_service = MuxService()
        for item in VIDEOS[:10]:
            action = ensure_video(db, mux_service, item, created_by)
            if action == "created":
                created += 1
            else:
                updated += 1
            print(f"{action}: {item['title']}")
    finally:
        db.close()

    print(f"Seed complete. created={created}, updated={updated}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
