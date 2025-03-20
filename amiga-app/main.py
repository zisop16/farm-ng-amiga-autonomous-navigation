# Copyright (c) farm-ng, inc.
#
# Licensed under the Amiga Development Kit License (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://github.com/farm-ng/amiga-dev-kit/blob/main/LICENSE
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path
from typing import Optional
import subprocess


import uvicorn
import os
from farm_ng.core.event_client_manager import (
    EventClient,
    EventClientSubscriptionManager,
)
from farm_ng.core.event_service_pb2 import EventServiceConfigList
from farm_ng.core.event_service_pb2 import SubscribeRequest
from farm_ng.core.events_file_reader import proto_from_json_file
from farm_ng.core.events_file_writer import proto_to_json_file
from farm_ng.core.event_service_pb2 import EventServiceConfig
from farm_ng.core.uri_pb2 import Uri
from farm_ng.track.track_pb2 import (
    Track,
    TrackFollowRequest,
)

from fastapi import FastAPI
from fastapi import WebSocket
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from google.protobuf.json_format import MessageToJson
from google.protobuf.json_format import ParseDict
from google.protobuf.empty_pb2 import Empty


# Path to the GPS logging script
SERVICE_CONFIG_PATH = os.getcwd() + "/service_config.json"

# Directory where track JSON files are stored
TRACKS_DIR = os.getcwd() + "/tracks/"

# Global process handler for Nav Logger
gps_logging_process: Optional[subprocess.Popen] = None

# Declare event_manager globally to avoid "not initialized" errors
event_manager: Optional[EventClientSubscriptionManager] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global event_manager
    print("Initializing App...")

    if event_manager:
        asyncio.create_task(event_manager.update_subscriptions())

    yield  # Allows FastAPI to properly initialize
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)

@app.get("/list_tracks")
async def list_tracks():
    """Lists all JSON track files in the `TRACKS_DIR` directory."""
    if not os.path.exists(TRACKS_DIR):
        return {"message": "No tracks directory found."}

    track_files = [f[:-5] for f in os.listdir(TRACKS_DIR) if f.endswith(".json")]

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
@app.post("/stop_recording")
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
    

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

if __name__ == "__main__":

    class Arguments:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)
    args=Arguments(
        config="/opt/farmng/config.json",
        port=8042,
        debug=False
    )

    # NOTE: we only serve the react app in debug mode
    if not args.debug:
        react_build_directory = Path(__file__).parent / "ts" / "dist"

        app.mount(
            "/",
            StaticFiles(directory=str(react_build_directory.resolve()), html=True),
        )
    # config with all the configs
    base_config_list: EventServiceConfigList = proto_from_json_file(
        args.config, EventServiceConfigList()
    )

    # filter out services to pass to the events client manager
    service_config_list = EventServiceConfigList()
    for config in base_config_list.configs:
        if config.port == 0:
            continue
        service_config_list.configs.append(config)

    event_manager = EventClientSubscriptionManager(config_list=service_config_list)

    # run the server
    uvicorn.run(app, host="0.0.0.0", port=args.port)  # noqa: S104
