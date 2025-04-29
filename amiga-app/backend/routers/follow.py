import asyncio
from pathlib import Path

from farm_ng.core.event_client_manager import EventClient
from farm_ng.core.events_file_reader import proto_from_json_file
from farm_ng.track.track_pb2 import (
    Track,
    TrackFollowRequest,
    TrackFollowerState
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
from backend.robot_utils import walk_towards
import base64



router = APIRouter()


@router.post("/follow/start/{track_name}")
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

    return {"message": f"Following track '{track_name}'."}

@router.get("/follow/state")
async def follower_state(request: Request):
    event_manager = request.state.event_manager
    client = event_manager.clients["track_follower"]

    state: TrackFollowerState = await client.request_reply("/get_state", Empty(), decode=True)
    
    controllable = state.status.robot_status.controllable
    
    return {"controllable": controllable}


@router.post("/follow/pause")
async def pause_following(request: Request):
    """Instructs the robot to pause track following."""
    event_manager = request.state.event_manager
    client = event_manager.clients["track_follower"]
    
    try:
        await client.request_reply("/pause", Empty())
    except AioRpcError:
        return {"error": "Not currently following a track"}

    return {"message": "Pausing track following"}

#Resume


@router.post("/follow/stop")
async def stop_following(request: Request):
    """Instructs the robot to stop track following."""
    event_manager = request.state.event_manager
    client = event_manager.clients["track_follower"]
    try:
        await client.request_reply("/cancel", Empty()), 0.5
    except AioRpcError:
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
        every_n (int, optional): the frequency to receive events.
    
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