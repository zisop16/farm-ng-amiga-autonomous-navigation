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
import json

# Path to the GPS logging script
NAV_LOGGER_SCRIPT = "main.py"
SERVICE_CONFIG_PATH = "gps_service_config.json"

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

# ### ✅ GPS Logger API ###
# @app.post("/start_nav_logger")
# async def start_nav_logger(background_tasks: BackgroundTasks) -> JSONResponse:
#     """Starts the GPS navigation logger process."""
#     global gps_logging_process

#     if gps_logging_process and gps_logging_process.poll() is None:
#         return JSONResponse(content={"message": "Nav Logger is already running!"}, status_code=400)

#     gps_logging_process = subprocess.Popen(
#         ["python", NAV_LOGGER_SCRIPT, "--service-config", SERVICE_CONFIG_PATH],
#         stdout=subprocess.PIPE,
#         stderr=subprocess.PIPE
#     )

#     return JSONResponse(content={"message": "Nav Logger started successfully!"}, status_code=200)

# @app.get("/stop_nav_logger")
# async def stop_nav_logger() -> JSONResponse:
#     """Stops the GPS navigation logger process."""
#     global gps_logging_process

#     if gps_logging_process and gps_logging_process.poll() is None:
#         gps_logging_process.terminate()
#         gps_logging_process = None
#         return JSONResponse(content={"message": "Nav Logger stopped."}, status_code=200)

#     return JSONResponse(content={"message": "Nav Logger is not running."}, status_code=400)

# @app.get("/logger_status")
# async def logger_status() -> JSONResponse:
#     """Returns the status of the Nav Logger."""
#     global gps_logging_process
#     if gps_logging_process and gps_logging_process.poll() is None:
#         return JSONResponse(content={"status": "running"}, status_code=200)
#     return JSONResponse(content={"status": "stopped"}, status_code=200)

# @app.get("/get_gps_log")
# async def get_gps_log() -> JSONResponse:
#     """Retrieve the logged GPS coordinates."""
#     log_file_path = "coordinates.txt"

#     if not Path(log_file_path).exists():
#         return JSONResponse(content={"message": "No GPS log available"}, status_code=404)

#     with open(log_file_path, "r") as log_file:
#         coordinates = log_file.readlines()

#     return JSONResponse(content={"gps_coordinates": coordinates}, status_code=200)



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

@app.get("/get_coordinates")
async def get_coordinates_file():
    coords_file_path = "./coordinates.txt"
    with open(coords_file_path, 'r') as coords_file:
        text = coords_file.read()
    return {
        "cords": text
    }



### ✅ Static File Serving ###
if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument("--config", type=Path, required=True, help="config file")
    # parser.add_argument("--port", type=int, default=8042, help="port to run the server")
    # parser.add_argument("--debug", action="store_true", help="debug mode")
    # args = parser.parse_args()

    # if not args.debug:
    #     react_build_directory = Path(__file__).parent / "ts" / "dist"
    #     app.mount(
    #         "/static",
    #         StaticFiles(directory=str(react_build_directory.resolve()), html=True),
    #     )

    # Initialize event manager properly
    # base_config_list: EventServiceConfigList = proto_from_json_file(
    #     args.config, EventServiceConfigList()
    # )

    # service_config_list = EventServiceConfigList()
    # for config in base_config_list.configs:
    #     if config.port == 0:
    #         continue
    #     service_config_list.configs.append(config)

    # event_manager = EventClientSubscriptionManager(config_list=service_config_list)
    port = 8000
    uvicorn.run(app, host="0.0.0.0", port=port)
