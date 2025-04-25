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
from fastapi import WebSocket
from farm_ng.core.event_service_pb2 import SubscribeRequest

from google.protobuf.json_format import MessageToJson
from farm_ng.core.uri_pb2 import Uri

from backend.config import *



router = APIRouter()

@router.post("/follow/{track_name}")
async def follow_track(request: Request, track_name: str):
    """Instructs the robot to follow an existing recorded track."""
    event_manager = request.state.event_manager

    track_path = Path(TRACKS_DIR) / f"{track_name}.json"
    client = event_manager.clients["track_follower"]

    if not track_path.exists():
        return {"error": f"Track: '{track_name} does not exist"}

    track: Track = proto_from_json_file(track_path, Track())

    await client.request_reply("/set_track", TrackFollowRequest(track=track))
    await client.request_reply("/start", Empty())

    return {"success": True, "message": f"Following track '{track_name}'."}


@router.post("/pause_following/")
async def pause_following(request: Request):
    """Instructs the robot to pause track following."""
    event_manager = request.state.event_manager
    client = event_manager.clients["track_follower"]
    
    await asyncio.wait_for(client.request_reply("/pause", Empty()), 0.5)

    return {"message": "Pausing track following"}


@router.post("/resume_following")
async def resume_following(request: Request):
    """Instructs the robot to resume track following."""
    event_manager = request.state.event_manager
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
    event_manager = request.state.event_manager
    client = event_manager.clients["track_follower"]
    try:
        await asyncio.wait_for(client.request_reply("/cancel", Empty()), 0.5)
    except asyncio.exceptions.TimeoutError:
        return {"success": False, "message": "Failed to call /cancel"}

    return {"success": True, "message": "Stopping track following"}

@router.websocket("/filter_data")
async def filter_data(
    websocket: WebSocket,
    every_n: int = 10
):
    """Coroutine to subscribe to filter state service via websocket.
    
    Args:
        websocket (WebSocket): the websocket connection
        every_n (int, optional): the frequency to receive events. Defaults to 1.
    
    Usage:
        ws = new WebSocket(`${API_URL}/filter_data`)
    """
    event_manager = websocket.state.event_manager
    full_service_name = "filter"
    client: EventClient = (event_manager.clients[full_service_name])

    await websocket.accept()

    # client.

    async for _, msg in client.subscribe(
        SubscribeRequest(
            uri=Uri(path=f"/state", query=f"service_name={full_service_name}"),
            every_n=every_n,
        ),
        decode=True,
    ):
        await websocket.send_json(MessageToJson(msg))

    await websocket.close()