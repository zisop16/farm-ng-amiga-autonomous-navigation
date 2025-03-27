import asyncio
from pathlib import Path

from farm_ng.core.event_client_manager import EventClient
from farm_ng.core.events_file_reader import proto_from_json_file
from farm_ng.track.track_pb2 import (
    Track,
    TrackFollowRequest,
)

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Request
from google.protobuf.empty_pb2 import Empty

from grpc.aio import AioRpcError

from backend.config import *


router = APIRouter()


@router.get("/follow/{track_name}")
async def follow_track(track_name: str):
    """Instructs the robot to follow an existing recorded track."""
    track_path = Path(TRACKS_DIR) / f"{track_name}.json"
    client = event_manager.clients["track_follower"]

    if not track_path.exists():
        raise HTTPException(status_code=404, detail=f"Track '{track_name}' not found.")

    track: Track = proto_from_json_file(track_path, Track())

    try:
        await client.request_reply("/set_track", TrackFollowRequest(track=track))
    except asyncio.exceptions.TimeoutError:
        return {"success": False, "message": "Failed to call /set_track"}
    except Exception as e:
        return {"success": False, "message": str(e)}

    try:
        await EventClient(config).request_reply("/start", Empty())
    except asyncio.exceptions.TimeoutError:
        return {"success": False, "message": "Failed to call /start"}

    return {"success": True, "message": f"Following track '{track_name}'."}


@router.post("/pause_following/")
async def pause_following(request: Request):
    """Instructs the robot to pause track following."""
    client = event_manager.clients["track_follower"]
    try:
        await asyncio.wait_for(client.request_reply("/pause", Empty()), 0.5)
    except AioRpcError as e:
        return {"success": False, "message": e.details()}
    except asyncio.exceptions.TimeoutError:
        return {"success": False, "message": "Failed to call /pause"}

    return {"success": True, "message": "Pausing track following"}


@router.post("/resume_following")
async def resume_following(request: Request):
    """Instructs the robot to resume track following."""
    client = event_manager.clients["track_follower"]
    try:
        await asyncio.wait_for(client.request_reply("/resume", Empty()), 0.5)
    except AioRpcError as e:
        return {"success": False, "message": e.details()}
    except asyncio.exceptions.TimeoutError:
        return {"success": False, "message": "Failed to call /resume"}

    return {"success": True, "message": "Resuming track following"}


@router.post("/stop_following")
async def stop_following(request: Request):
    """Instructs the robot to stop track following."""
    client = event_manager.clients["track_follower"]
    try:
        await asyncio.wait_for(client.request_reply("/cancel", Empty()), 0.5)
    except asyncio.exceptions.TimeoutError:
        return {"success": False, "message": "Failed to call /cancel"}

    return {"success": True, "message": "Stopping track following"}
