from __future__ import annotations

import argparse
import asyncio
import subprocess
from pathlib import Path
from typing import Optional

import uvicorn
from farm_ng.core.event_client_manager import EventClientSubscriptionManager
from farm_ng.core.event_service_pb2 import EventServiceConfigList, SubscribeRequest
from farm_ng.core.events_file_reader import proto_from_json_file
from farm_ng.core.uri_pb2 import Uri
from fastapi import FastAPI, BackgroundTasks, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from google.protobuf.json_format import MessageToJson
from contextlib import asynccontextmanager
import os
from pathlib import Path
import json
##added

import asyncio
from pathlib import Path
from fastapi import HTTPException

from farm_ng.core.event_client import EventClient
from farm_ng.core.event_service_pb2 import EventServiceConfig
from farm_ng.core.events_file_reader import proto_from_json_file
from farm_ng.core.events_file_writer import proto_to_json_file
from farm_ng.core.pose_pb2 import Pose
from farm_ng.track.track_pb2 import (
    Track,
    TrackFollowRequest,
)

from google.protobuf.empty_pb2 import Empty
from farm_ng.track.track_pb2 import Track
from google.protobuf.json_format import ParseDict


# Path to the GPS logging script
SERVICE_CONFIG_PATH = "/mnt/managed_home/farm-ng-user-munir-khan/farm-ng-amiga-autonomous-navigation/amiga-app/service_config.json"

# Global process handler for Nav Logger
gps_logging_process: Optional[subprocess.Popen] = None

# Declare event_manager globally to avoid "not initialized" errors
event_manager: Optional[EventClientSubscriptionManager] = None

# Use lifespan instead of @app.on_event("startup")
@asynccontextmanager
async def lifespan(app: FastAPI):
    global event_manager
    print("Initializing App...")

    if event_manager:
        asyncio.create_task(event_manager.update_subscriptions())

    yield  # Allows FastAPI to properly initialize
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




# Directory where track JSON files are stored
TRACKS_DIR = "/mnt/managed_home/farm-ng-user-munir-khan/farm-ng-amiga-autonomous-navigation/amiga-app/tracks"

@app.get("/list_tracks")
async def list_tracks():
    """Lists all JSON track files in the `TRACKS_DIR` directory."""
    if not os.path.exists(TRACKS_DIR):
        return {"message": "No tracks directory found."}

    track_files = [f for f in os.listdir(TRACKS_DIR) if f.endswith(".json")]

    if not track_files:
        return {"message": "No tracks available."}

    return {"tracks": track_files}

@app.get("/get_track/{track_name}")
async def get_track(track_name: str):
    """Reads a track JSON file and returns its content."""
    track_path = os.path.join(TRACKS_DIR, f"{track_name}.json")

    if not os.path.exists(track_path):
        return {"message": f"Track '{track_name}.json' not found."}

    with open(track_path, "r") as json_file:
        track_data = json.load(json_file)

    waypoints = track_data.get("waypoints", [])

    return {
        "track_name": track_name,
        "waypoints": waypoints
    }


###
recording_active = False
@app.post("/record/{track_name}")
async def start_recording(track_name: str, background_tasks: BackgroundTasks):
    """Starts recording a track using the filter service client."""
    global recording_active
    if recording_active:
        raise HTTPException(status_code=400, detail="Recording is already in progress.")

    recording_active = True  # Set recording flag to true
    output_dir = Path(TRACKS_DIR)

    service_config_path = Path(SERVICE_CONFIG_PATH)
    if not service_config_path.exists():
        raise HTTPException(status_code=500, detail="Service configuration file not found.")

    # Run the recording as a background task
    background_tasks.add_task(record_track, service_config_path, track_name, output_dir)

    return {"message": f"Recording started for track '{track_name}'."}


async def record_track(service_config_path: Path, track_name: str, output_dir: Path) -> None:
    """Runs the filter service client to record a track."""
    global recording_active
    recording_active = True  # Ensure we mark recording as active

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load the service configuration
    with open(service_config_path, "r") as f:
        service_configs = json.load(f)

    # Extract the "filter" service configuration
    filter_config_dict = next((cfg for cfg in service_configs if cfg.get("name") == "filter"), None)

    if not filter_config_dict:
        raise HTTPException(status_code=500, detail="Filter service configuration not found.")

    # Convert dictionary to protobuf format
    config: EventServiceConfig = EventServiceConfig()
    ParseDict(filter_config_dict, config)

    # Clear the track before recording
    try:
        print(f"Sending /clear_track request to {config.host}:{config.port}")
        await asyncio.wait_for(EventClient(config).request_reply("/clear_track", Empty()), timeout=5)
    except asyncio.TimeoutError:
        print("⚠ Timeout: No response from /clear_track. Continuing recording.")

    # Create a Track message
    track = Track()

    # Subscribe to the filter track topic
    async for event, message in EventClient(config).subscribe(config.subscriptions[0], decode=True):
        if not recording_active:
            print("Recording stopped.")
            break  # Stop recording loop

        print("Adding to track:", message)
        next_waypoint = track.waypoints.add()
        next_waypoint.CopyFrom(message)

        track_file = output_dir / f"{track_name}.json"
        if not proto_to_json_file(track_file, track):
            print(f"⚠ Failed to write Track to {track_file}")
            break  # Stop recording if writing fails

        print(f"✅ Saved track of length {len(track.waypoints)} to {track_file}")

    print("Recording task completed.")
###stop###
async def stop_recording():
    """Stops the recording process."""
    global recording_active
    if not recording_active:
        return {"message": "No recording in progress."}

    recording_active = False  # Stop the recording process
    return {"message": "Recording stopped successfully."}

###Follow a Track ###
@app.get("/follow/{track_name}")
async def follow_track(track_name: str):
    """Instructs the robot to follow an existing recorded track."""
    track_path = Path(TRACKS_DIR) / f"{track_name}.json"
    service_config_path = Path(SERVICE_CONFIG_PATH)

    if not track_path.exists():
        raise HTTPException(status_code=404, detail=f"Track '{track_name}' not found.")

    # Load the service configuration
    with open(service_config_path, "r") as f:
        service_configs = json.load(f)

    # Find the "track_follower" configuration
    target_cfg = None
    for cfg in service_configs:
        if cfg.get("name") == "track_follower":
            target_cfg = cfg
            break

    if target_cfg is None:
        raise HTTPException(status_code=500, detail="Track follower configuration not found.")

    config: EventServiceConfig = ParseDict(target_cfg, EventServiceConfig())
    track: Track = proto_from_json_file(track_path, Track())

    try:
        await EventClient(config).request_reply("/set_track", TrackFollowRequest(track=track))
    except asyncio.exceptions.TimeoutError:
        return {"success": False, "message": "Failed to call /set_track"}
    except Exception as e:
        return {"success": False, "message": str(e)}

    try:
        await EventClient(config).request_reply("/start", Empty())
    except asyncio.exceptions.TimeoutError:
        return {"success": False, "message": "Failed to call /start"}

    return {"sucess": True, "message": f"Following track '{track_name}'."}
    
###


### ✅ Static File Serving ###
if __name__ == "__main__":

    port = 8000
    uvicorn.run(app, host="0.0.0.0", port=port)