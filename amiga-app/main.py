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
import signal
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

import fastapi
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
from pydantic import BaseModel
from grpc.aio import AioRpcError


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
    calibrated = await event_manager.clients["filter"].request_reply("/calibrate", Empty())
    print(calibrated)


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


# Define Pydantic model for request data
class EditTrackRequest(BaseModel):
    current_name: str
    new_name: str

# Only one definition of the endpoint
@app.post("/edit_track")
async def edit_track_name(request: EditTrackRequest):
    current_name = request.current_name
    new_name = request.new_name

    track_path = os.path.join(TRACKS_DIR, f"{current_name}.json")
    new_track_path = os.path.join(TRACKS_DIR, f"{new_name}.json")

    # Check if the current track file exists
    if not os.path.exists(track_path):
        raise HTTPException(status_code=404, detail="Track not found.")
    
    # Check if the new track name already exists
    if os.path.exists(new_track_path):
        raise HTTPException(status_code=400, detail="A track with the new name already exists.")

    try:
        # Rename the file
        os.rename(track_path, new_track_path)
        return {"message": f"Track renamed from '{current_name}' to '{new_name}'."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))





###
recording_active = False
recording_task = None  # Track the recording task

@app.post("/record/{track_name}")
async def start_recording(track_name: str):
    """Starts recording a track using the filter service client."""
    global recording_active, recording_task
    if recording_active:
        raise HTTPException(status_code=400, detail="Recording is already in progress.")

    recording_active = True  # Set recording flag to true
    output_dir = Path(TRACKS_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists

    service_config_path = Path(SERVICE_CONFIG_PATH)
    if not service_config_path.exists():
        raise HTTPException(status_code=500, detail="Service configuration file not found.")

    # Start the recording as an asyncio task
    recording_task = asyncio.create_task(record_track(service_config_path, track_name, output_dir))
    print(f"Recording started for track '{track_name}'")
    return {"message": f"Recording started for track '{track_name}'."}

async def record_track(service_config_path: Path, track_name: str, output_dir: Path) -> None:
    """Runs the filter service client to record a track."""
    global recording_active
    recording_active = True  # Ensure we mark recording as active

    # Create a Track message
    track = Track()

    try:
        # Establish a WebSocket connection to the existing filter_data endpoint
        print("Connecting to the filter data WebSocket...")
        async with websockets.connect("ws://localhost:8000/filter_data") as websocket:
            print("Connected to filter data WebSocket for recording.")
            while recording_active:
                try:
                    message = await websocket.recv()
                    print("Received message from WebSocket:", message)
                    msg_data = json.loads(message)

                    # Add the message to the track waypoints
                    next_waypoint = track.waypoints.add()
                    next_waypoint.CopyFrom(msg_data)

                    # Write the track to a file
                    track_file = output_dir / f"{track_name}.json"
                    if not proto_to_json_file(track_file, track):
                        print(f"⚠ Failed to write Track to {track_file}")
                        break  # Stop recording if writing fails

                    print(f"✅ Saved track of length {len(track.waypoints)} to {track_file}")
                except Exception as e:
                    print(f"Error during track recording: {str(e)}")
                    break
    except Exception as e:
        print(f"Error connecting to WebSocket: {str(e)}")
    finally:
        recording_active = False
        print("Recording task completed.")




@app.post("/stop_recording")
async def stop_recording():
    """Stops the recording process."""
    global recording_active, recording_task
    if not recording_active:
        return {"message": "No recording in progress."}

    recording_active = False  # Stop the recording process
    if recording_task:
        recording_task.cancel()  # Cancel the running task if it exists
        try:
            await recording_task  # Ensure the task is cleaned up
        except asyncio.CancelledError:
            print("Recording task was canceled.")

    recording_task = None  # Clear the task reference
    return {"message": "Recording stopped successfully."}




@app.websocket("/filter_data")
async def filter_data(
    websocket: WebSocket,
    every_n: int = 7
):
    """Coroutine to subscribe to filter state service via websocket.
    
    Args:
        websocket (WebSocket): the websocket connection
        every_n (int, optional): the frequency to receive events. Defaults to 1.
    
    Usage:
        ws = new WebSocket(`${API_URL}/filter_data`)
    """

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


###FOLLOW HERE
@app.post("/follow/{track_name}")
async def follow_track(track_name: str):
    """Instructs the robot to follow an existing recorded track."""
    track_path = Path(TRACKS_DIR) / f"{track_name}.json"
    
    # Check if the track file exists
    if not track_path.exists():
        raise HTTPException(status_code=404, detail=f"Track '{track_name}' not found.")

    # Load the track data
    try:
        track: Track = proto_from_json_file(track_path, Track())
    except Exception as e:
        return {"success": False, "message": f"Failed to load track file: {str(e)}"}

    # Get the track follower client
    client = event_manager.clients.get("track_follower")
    if client is None:
        return {"success": False, "message": "Track follower client not found."}

    # Set the track for following
    try:
        await client.request_reply("/set_track", TrackFollowRequest(track=track))
    except asyncio.exceptions.TimeoutError:
        return {"success": False, "message": "Failed to call /set_track"}
    except Exception as e:
        return {"success": False, "message": str(e)}

    # Start following the track
    try:
        await client.request_reply("/start", Empty())
    except asyncio.exceptions.TimeoutError:
        return {"success": False, "message": "Failed to call /start"}
    except Exception as e:
        return {"success": False, "message": str(e)}

    return {"success": True, "message": f"Following track '{track_name}'."}

@app.post("/pause_following/")
async def pause_following():
    """Instructs the robot to pause track following."""
    print("Attempting to pause track following...")
    if event_manager is None:
        print("Event manager is not initialized.")
        return {"success": False, "message": "Event manager not initialized."}

    client = event_manager.clients.get("track_follower")
    if client is None:
        print("Track follower client not found.")
        return {"success": False, "message": "Track follower client not found."}

    try:
        print("Sending pause command to track follower...")
        await asyncio.wait_for(client.request_reply("/pause", Empty()), 0.5)
        print("Pause command sent successfully.")
    except AioRpcError as e:
        print(f"Error during pause: {e.details()}")
        return {"success": False, "message": e.details()}
    except asyncio.exceptions.TimeoutError:
        print("Timeout during pause")
        return {"success": False, "message": "Failed to call /pause"}

    print("Track following paused successfully.")
    return {"success": True, "message": "Pausing track following"}

@app.post("/resume_following")
async def resume_following():
    """Instructs the robot to resume track following."""
    print("Attempting to resume track following...")
    if event_manager is None:
        print("Event manager is not initialized.")
        return {"success": False, "message": "Event manager not initialized."}

    client = event_manager.clients.get("track_follower")
    if client is None:
        print("Track follower client not found.")
        return {"success": False, "message": "Track follower client not found."}

    try:
        print("Sending resume command to track follower...")
        await asyncio.wait_for(client.request_reply("/resume", Empty()), 0.5)
        print("Resume command sent successfully.")
    except AioRpcError as e:
        print(f"Error during resume: {e.details()}")
        return {"success": False, "message": e.details()}
    except asyncio.exceptions.TimeoutError:
        print("Timeout during resume")
        return {"success": False, "message": "Failed to call /resume"}

    print("Track following resumed successfully.")
    return {"success": True, "message": "Resuming track following"}


####
@app.get("/kill")
async def kill():
    os.kill(os.getpid(), signal.SIGTERM)
    return fastapi.Response(status_code=200, content='Server shutting down...')

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
        port=8000,
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
