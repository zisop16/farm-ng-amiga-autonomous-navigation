from fastapi import APIRouter
from fastapi import HTTPException
import json
from pathlib import Path

from backend.config import *

router = APIRouter()


@router.get("/list_tracks")
async def list_tracks():
    """Lists all JSON track files in the `TRACKS_DIR` directory."""
    if not os.path.exists(TRACKS_DIR):
        return {"message": "No tracks directory found."}

    track_files = [f[:-5] for f in os.listdir(TRACKS_DIR) if f.endswith(".json")]

    if not track_files:
        return {"message": "No tracks available."}

    return {"tracks": track_files}


@router.get("/delete_track/{track_name}")
async def delete_track(track_name: str):
    """Deletes a JSON track file from the  `TRACKS_DIR` directory."""
    if not track_name:
        raise HTTPException(status_code=400, detail="Empty path name passed")
    track_name = track_name.strip()
    json_path = Path(TRACKS_DIR) / (track_name + ".json")

    if (
        not json_path.resolve().parent == Path(TRACKS_DIR)
        or not json_path.resolve().is_absolute()
    ):
        raise HTTPException(
            status_code=403, detail="Trying to delete file outside tracks directory"
        )

    if not json_path.exists():
        raise HTTPException(status_code=404, detail="File does not exist")

    try:
        json_path.unlink()
    except Exception as e:
        return {"success": False, "message": str(e)}

    return {"success": True, "message": "Track deleted", "track_name": track_name}


@router.get("/get_track/{track_name}")
async def get_track(track_name: str):
    """Reads a track JSON file and returns its content."""
    track_path = os.path.join(TRACKS_DIR, f"{track_name}.json")

    if not os.path.exists(track_path):
        return {"message": f"Track '{track_name}.json' not found."}

    with open(track_path, "r") as json_file:
        track_data = json.load(json_file)

    waypoints = track_data.get("waypoints", [])

    return {"track_name": track_name, "waypoints": waypoints}
