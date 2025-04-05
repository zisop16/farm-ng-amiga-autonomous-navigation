import asyncio
import json

from farm_ng.core.event_client_manager import EventClient
from farm_ng.core.events_file_writer import proto_to_json_file
from farm_ng.core.event_service_pb2 import EventServiceConfig
from farm_ng.track.track_pb2 import Track
from farm_ng.filter.filter_pb2 import FilterState
from farm_ng_core_pybind import Isometry3F64
from farm_ng_core_pybind import Pose3F64
from farm_ng_core_pybind import Rotation3F64
import numpy as np

from fastapi import HTTPException
from fastapi import BackgroundTasks
from fastapi import APIRouter
from fastapi import Request

from google.protobuf.json_format import ParseDict
from google.protobuf.empty_pb2 import Empty

from pathlib import Path

from backend.config import *

router = APIRouter()

async def get_pose(filter_client: EventClient) -> Pose3F64:
    """Get the current pose of the robot in the world frame, from the filter service.

    Args:
        filter_client: EventClient for the filter service
    """
    # We use the FilterState as the best source of the current pose of the robot
    state: FilterState = await filter_client["filter"].request_reply("/get_state", Empty(), decode=True)
    return Pose3F64.from_proto(state.pose)


@router.post("/line/record/{track_name}")
async def start_recording(track_name: str, background_tasks: BackgroundTasks):
    """Starts recording a track using the filter service client."""
    global recording_active
    if recording_active:
        raise HTTPException(status_code=400, detail="Recording is already in progress.")

    recording_active = True  # Set recording flag to true
    output_dir = Path(LINES_DIR)

    service_config_path = Path(SERVICE_CONFIG_PATH)

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
    print(f"Sending /clear_track request to {config.host}:{config.port}")
    await EventClient(config).request_reply("/clear_track", Empty())

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
@router.post("/line/stop_record")
async def stop_recording(request: Request):
    """Stops the recording process."""
    recording_active = request.state["vars"]["line_recording"]
    if not recording_active:
        return {"message": "No recording in progress."}

    recording_active = False  # Stop the recording process
    return {"message": "Recording stopped successfully."}

@router.post("/line/calibrate_turn/start")
async def calibrate_turn(request: Request):
    if request.state["vars"]["turn_calibrating"]:
        return {"error": "Turn calibration is already active"}
    filter_client = request.state["event_manager"].clients["filter"]
    request.state["vars"]["turn_calibration_start"] = await get_pose(filter_client)
    request.state["vars"]["turn_calibration_segments"] = 1
    request.state["vars"]["turn_calibrating"] = True
    return {"message": "Turn calibration started."}

@router.post("/line/calibrate_turn/segment")
async def add_turn_segment(request: Request):
    if not request.state["vars"]["turn_calibrating"]:
        return {"error": "Turn calibration is not active."}
    request.state["vars"]["turn_calibration_segments"] += 1

@router.post("/line/calibrate_turn/end")
async def end_turn_calibration(request: Request):
    if not request.state["vars"]["turn_calibrating"]:
        return {"error": "Turn calibration is not active"}
    filter_client = request.state["event_manager"].clients["filter"]
    request.state["vars"]["turn_calibrating"] = False
    num_segments = request.state["vars"]["turn_calibration_segments"]
    start_position = request.state["vars"]["turn_calibration_start"].translation
    end_position = (await get_pose(filter_client)).translation
    turn_diff = np.array(end_position) - np.array(start_position)
    line_waypoints = request.state["vars"]["active_line"]
    line_start = line_waypoints[0].translation
    line_end = line_waypoints[1].translation
    line_diff = np.array(line_end) - np.array(line_start)
    line_direction = line_diff / np.linalg.norm(line_diff)
    left_turn_direction = np.array((-line_direction[1], line_direction[0]))
    turn_length = np.abs((turn_diff / num_segments).dot(left_turn_direction))
    request.state["vars"]["turn_length"] = turn_length
    return {"message": "Turn calibration complete."}


async def build_square(clients: dict[str, EventClient], side_length: float, clockwise: bool) -> Track:
    """Build a square track, from the current pose of the robot.

    Args:
        clients (dict[str, EventClient]): A dictionary of EventClients.
        side_length (float): The side length of the square, in meters.
        clockwise (bool): True will drive the square clockwise (right hand turns).
                        False is counter-clockwise (left hand turns).
    Returns:
        Track: The track for the track_follower to follow.
    """

    # Query the state estimation filter for the current pose of the robot in the world frame
    world_pose_robot: Pose3F64 = await get_pose(clients)

    # Create a container to store the track waypoints
    track_waypoints: list[Pose3F64] = []

    # Set the angle of the turns, based on indicated direction
    angle: float = -np.pi/2 if clockwise else np.pi/2

    # Add the first goal at the current pose of the robot
    world_pose_goal0: Pose3F64 = world_pose_robot * Pose3F64(a_from_b=Isometry3F64(), frame_a="robot", frame_b="goal0")
    track_waypoints.append(world_pose_goal0)

    # Drive forward 1 meter (first side of the square)
    track_waypoints.extend(create_straight_segment(track_waypoints[-1], "goal1", side_length))

    # Turn left 90 degrees (first turn)
    track_waypoints.extend(create_turn_segment(track_waypoints[-1], "goal2", angle))

    # Add second side and turn
    track_waypoints.extend(create_straight_segment(track_waypoints[-1], "goal3", side_length))
    track_waypoints.extend(create_turn_segment(track_waypoints[-1], "goal4", angle))

    # Add third side and turn
    track_waypoints.extend(create_straight_segment(track_waypoints[-1], "goal5", side_length))
    track_waypoints.extend(create_turn_segment(track_waypoints[-1], "goal6", angle))

    # Add fourth side and turn
    track_waypoints.extend(create_straight_segment(track_waypoints[-1], "goal7", side_length))
    track_waypoints.extend(create_turn_segment(track_waypoints[-1], "goal8", angle))

    # Return the list of waypoints as a Track proto message
    return format_track(track_waypoints)


def create_straight_segment(
    previous_pose: Pose3F64, next_frame_b: str, distance: float, spacing: float = 0.1
) -> list[Pose3F64]:
    """Compute a straight segment of a square.

    Args:
        previous_pose (Pose3F64): The previous pose.
        next_frame_b (str): The name of the child frame of the next pose.
        distance (float): The side length of the square, in meters.
        spacing (float): The spacing between waypoints, in meters.

    Returns:
        Pose3F64: The poses of the straight segment.
    """
    # Create a container to store the track segment waypoints
    segment_poses: list[Pose3F64] = [previous_pose]

    # For tracking the number of segments and remaining angle
    counter: int = 0
    remaining_distance: float = distance

    while abs(remaining_distance) > 0.01:
        # Compute the distance of the next segment
        segment_distance: float = copysign(min(abs(remaining_distance), spacing), distance)

        # Compute the next pose
        straight_segment: Pose3F64 = Pose3F64(
            a_from_b=Isometry3F64([segment_distance, 0, 0], Rotation3F64.Rz(0)),
            frame_a=segment_poses[-1].frame_b,
            frame_b=f"{next_frame_b}_{counter}",
        )
        segment_poses.append(segment_poses[-1] * straight_segment)

        # Update the counter and remaining angle
        counter += 1
        remaining_distance -= segment_distance

    # Rename the last pose to the desired name
    segment_poses[-1].frame_b = next_frame_b
    return segment_poses


def create_turn_segment(
    previous_pose: Pose3F64, next_frame_b: str, angle: float, spacing: float = 0.1
) -> list[Pose3F64]:
    """Compute a turn segment

    Args:
        previous_pose (Pose3F64): The previous pose.
        next_frame_b (str): The name of the child frame of the next pose.
        angle (float): The angle to turn, in radians (+ left, - right).
        spacing (float): The spacing between waypoints, in radians.
    Returns:
        list[Pose3F64]: The poses of the turn segment.
    """
    # Create a container to store the track segment waypoints
    segment_poses: list[Pose3F64] = [previous_pose]

    # For tracking the number of segments and remaining angle
    counter: int = 0
    remaining_angle: float = angle

    while abs(remaining_angle) > 0.01:
        # Compute the angle of the next segment
        segment_angle: float = copysign(min(abs(remaining_angle), spacing), angle)

        # Compute the next pose
        turn_segment: Pose3F64 = Pose3F64(
            a_from_b=Isometry3F64.Rz(segment_angle),
            frame_a=segment_poses[-1].frame_b,
            frame_b=f"{next_frame_b}_{counter}",
        )
        segment_poses.append(segment_poses[-1] * turn_segment)

        # Update the counter and remaining angle
        counter += 1
        remaining_angle -= segment_angle

    # Rename the last pose to the desired name
    segment_poses[-1].frame_b = next_frame_b
    return segment_poses