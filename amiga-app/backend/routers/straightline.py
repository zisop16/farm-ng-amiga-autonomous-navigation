import asyncio
import json

from farm_ng.core.event_client_manager import EventClient
from farm_ng.core.events_file_writer import proto_to_json_file
from farm_ng.core.event_service_pb2 import EventServiceConfig
from farm_ng.track.track_pb2 import Track

from fastapi import HTTPException
from fastapi import BackgroundTasks
from fastapi import APIRouter

from google.protobuf.json_format import ParseDict
from google.protobuf.empty_pb2 import Empty

from pathlib import Path

from backend.config import *

router = APIRouter()

recording_active = False

@router.post("/record_line/{track_name}")
async def start_recording(track_name: str, background_tasks: BackgroundTasks):
    """Starts recording a track using the filter service client."""
    global recording_active
    if recording_active:
        raise HTTPException(status_code=400, detail="Recording is already in progress.")

    recording_active = True  # Set recording flag to true
    output_dir = Path(TRACKS_DIR)

    service_config_path = Path(SERVICE_CONFIG_PATH)
    if not service_config_path.exists():
        raise HTTPException(
            status_code=500, detail="Service configuration file not found."
        )

    # Run the recording as a background task
    background_tasks.add_task(record_track, service_config_path, track_name, output_dir)

    return {"message": f"Recording started for track '{track_name}'."}

async def record_track(
    service_config_path: Path, track_name: str, output_dir: Path
) -> None:
    """Runs the filter service client to record a track."""
    global recording_active
    recording_active = True  # Ensure we mark recording as active

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load the service configuration
    with open(service_config_path, "r") as f:
        service_configs = json.load(f)

    # Extract the "filter" service configuration
    filter_config_dict = next(
        (cfg for cfg in service_configs if cfg.get("name") == "filter"), None
    )

    if not filter_config_dict:
        raise HTTPException(
            status_code=500, detail="Filter service configuration not found."
        )

    # Convert dictionary to protobuf format
    config: EventServiceConfig = EventServiceConfig()
    ParseDict(filter_config_dict, config)

    # Clear the track before recording
    try:
        print(f"Sending /clear_track request to {config.host}:{config.port}")
        await asyncio.wait_for(
            EventClient(config).request_reply("/clear_track", Empty()), timeout=5
        )
    except asyncio.TimeoutError:
        print("⚠ Timeout: No response from /clear_track. Continuing recording.")

    # Create a Track message
    track = Track()

    # Subscribe to the filter track topic
    async for event, message in EventClient(config).subscribe(
        config.subscriptions[0], decode=True
    ):
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
@router.post("/stop_recording")
async def stop_recording():
    """Stops the recording process."""
    global recording_active
    if not recording_active:
        return {"message": "No recording in progress."}

    recording_active = False  # Stop the recording process
    return {"message": "Recording stopped successfully."}