from typing import Tuple
import requests
from app.core.config import settings


class MuxService:
    def __init__(self) -> None:
        self.base_url = "https://api.mux.com/video/v1"
        self.auth = (settings.mux_token_id, settings.mux_token_secret)

    def create_asset(self, input_url: str) -> Tuple[str, str]:
        payload = {
            "input": [{"url": input_url}],
            "playback_policy": ["public"],
        }
        response = requests.post(
            f"{self.base_url}/assets",
            json=payload,
            auth=self.auth,
            timeout=30,
        )
        if not response.ok:
            raise RuntimeError(f"Mux error {response.status_code}: {response.text}")
        data = response.json()["data"]
        mux_asset_id = data["id"]
        playback_id = data["playback_ids"][0]["id"]
        return mux_asset_id, playback_id

    def get_asset_status(self, mux_asset_id: str) -> str:
        response = requests.get(
            f"{self.base_url}/assets/{mux_asset_id}",
            auth=self.auth,
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()["data"]
        return data.get("status", "processing")

    @staticmethod
    def get_public_playback_url(playback_id: str) -> str:
        return f"https://stream.mux.com/{playback_id}.m3u8"
