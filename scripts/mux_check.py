import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import requests
from app.core.config import settings


def main() -> int:
    url = "https://api.mux.com/video/v1/assets"
    auth = (settings.mux_token_id, settings.mux_token_secret)
    response = requests.get(url, auth=auth, timeout=30)
    if not response.ok:
        print(f"Mux error {response.status_code}: {response.text}")
        return 1

    data = response.json().get("data", [])
    print(f"Mux assets count: {len(data)}")
    for item in data[:10]:
        asset_id = item.get("id")
        status = item.get("status")
        playback_ids = item.get("playback_ids") or []
        playback_id = playback_ids[0].get("id") if playback_ids else None
        print(f"- {asset_id} | {status} | playback_id={playback_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
