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
from farm_ng.core.event_service_pb2 import SubscribeRequest
from farm_ng.core.uri_pb2 import Uri
from farm_ng.core.events_file_reader import proto_from_json_file

import numpy as np

from fastapi import HTTPException
from fastapi import BackgroundTasks
from fastapi import APIRouter
from fastapi import Request

from pydantic import BaseModel

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
    state: FilterState = await filter_client.request_reply("/get_state", Empty(), decode=True)
    return Pose3F64.from_proto(state.pose)


@router.post("/line/record/{track_name}")
async def start_recording(request: Request, track_name: str, background_tasks: BackgroundTasks):
    """Starts recording a track using the filter service client."""
    vars: StateVars = request.state.vars
    if vars.line_recording is not None:
        raise HTTPException(status_code=400, detail="Recording is already in progress.")

    vars.line_recording = track_name  # Set recording flag to true
    
    client = request.state.event_manager.clients["filter"]
    vars.line_start = (await get_pose(client)).translation

    return {"message": f"Recording started for track '{track_name}'."}




###stop###
@router.post("/line/record/stop")
async def stop_recording(request: Request):
    """Stops the recording process."""
    vars: StateVars = request.state["vars"]
    if not vars.line_recording:
        return {"message": "No recording in progress."}

    vars.line_recording = None  # Stop the recording process
    client = request.state.event_manager.clients["filter"]
    vars.line_end = (await get_pose(client)).translation
    return {"message": "Recording stopped successfully."}

@router.post("/line/calibrate_turn/start")
async def calibrate_turn(request: Request):
    vars: StateVars = request.state["vars"]
    if vars.turn_calibrating:
        return {"error": "Turn calibration is already active"}
    filter_client = request.state["event_manager"].clients["filter"]
    vars.turn_calibration_start = await get_pose(filter_client)
    vars.turn_calibration_segments = 1
    vars.turn_calibrating = True
    return {"message": "Turn calibration started."}

@router.post("/line/calibrate_turn/segment")
async def add_turn_segment(request: Request):
    vars: StateVars = request.state["vars"]
    if not vars.turn_calibrating:
        return {"error": "Turn calibration is not active."}
    vars.turn_calibration_segments += 1

@router.post("/line/calibrate_turn/end")
async def end_turn_calibration(request: Request):
    vars: StateVars = request.state["vars"]
    if not vars.turn_calibrating:
        return {"error": "Turn calibration is not active"}
    filter_client = request.state["event_manager"].clients["filter"]
    vars.turn_calibrating = False
    num_segments = vars.turn_calibration_segments
    start_position = vars.turn_calibration_start.translation
    end_position = (await get_pose(filter_client)).translation
    turn_diff = np.array(end_position) - np.array(start_position)
    line_diff = np.array(vars.line_end) - np.array(vars.line_start)
    line_direction = line_diff / np.linalg.norm(line_diff)
    left_turn_direction = np.array((-line_direction[1], line_direction[0]))
    turn_length = np.abs((turn_diff / num_segments).dot(left_turn_direction))
    vars.turn_length = turn_length

    line_data = {
        "start": vars.line_start,
        "end": vars.line_end,
        "turn_length": turn_length
    }
    json_text = json.dumps(line_data)
    output_dir = Path(LINES_DIR)
    json_path = output_dir / f"{vars.line_recording}.json"
    with open(json_path, 'w') as line_file:
        line_file.write(json_text)

    return {"message": "Turn calibration complete."}

class LineFollowData(BaseModel):
    num_rows: int
    first_turn_right: bool
@router.post("/line/follow/{line_name}")
async def follow_line(request: Request, line_name: str):
    vars: StateVars = request.state["vars"]
    if (vars.following_line):
        return {"error": "Line is currently being followed"}
    
    
    line_path = Path(LINES_DIR) / f"{line_name}.json"
    
    if not line_path.exists():
        return {"error": f"Track: '{line_name} does not exist"}

    with open(line_path, 'r') as line_file:
        line_data = json.loads(line_file.read())
    line_start = line_data["start"]
    line_end = line_data["end"]
    turn_length = line_data["turn_length"]

    if vars.following_line:
        return {"error": "Line is currently being followed"}


    from_waypoint_0 = Pose3F64(
        a_from_b=Isometry3F64(line_start, Rotation3F64.Rz(0))^-1
    )

    remaining_rows = data.num_rows
    event_manager = request.state.event_manager
    filter_client = event_manager.clients["filter"]

    current_pose = await get_pose(filter_client)
    total_path: list[Pose3F64] = walk_towards(current_pose, line_start)
    world_pose_robot = await get_pose(filter_client)
    world_pose_goal0 = Pose3F64(
        a_from_b=Isometry3F64(
            world_pose_robot.translation,
            vars.active_line[0].rotation
        ), 
        frame_a="robot",
        frame_b="goal0"
    )
    total_path.append(world_pose_goal0)

    while remaining_rows >= 3:
        total_path.extend(build_two_turns(vars, data.first_turn_right))
        remaining_rows -= 2

def walk_towards(current_pose: Pose3F64, position: list[float]) -> list[Pose3F64]:
    """_summary_
    Given the robot's current pose, outputs the list of poses the robot must use in their track to walk towards the target position
    Args:
        current_pose (Pose3F64): Current position / rotation of robot
        position (list[float]): Target position

    Returns:
        list[Pose3F64]
    """
    current_position = np.array(current_pose.translation)
    target_position = np.array(position)
    current_rotation = current_pose.rotation
    diff = target_position - current_position
    distance = np.linalg.norm(diff)
    current_angle = 
    


async def build_two_turns(vars: StateVars, turn_right: bool) -> list[Pose3F64]:
    """Build a square track, from the current pose of the robot.

    Args:
        clients (dict[str, EventClient]): A dictionary of EventClients.
        side_length (float): The side length of the square, in meters.
        clockwise (bool): True will drive the square clockwise (right hand turns).
                        False is counter-clockwise (left hand turns).
    Returns:
        Track: The track for the track_follower to follow.
    """

    # Create a container to store the track waypoints
    track_waypoints: list[Pose3F64] = []

    # Set the angle of the turns, based on indicated direction
    angle: float = -np.pi/2 if turn_right else np.pi/2

    # Drive forward 1 meter (first side of the square)
    track_waypoints.extend(create_line_segment(track_waypoints[-1], "goal1", vars.active_line))

    # Turn 90 degrees (first turn)
    track_waypoints.extend(create_turn_segment(track_waypoints[-1], "goal2", angle))

    # Add second line and turn
    track_waypoints.extend(create_line_segment(track_waypoints[-1], "goal3", vars.active_line))
    track_waypoints.extend(create_turn_segment(track_waypoints[-1], "goal4", angle))

    # Return the list of waypoints as a Track proto message
    return track_waypoints



def create_straight_segment(
    previous_pose: Pose3F64, distance: float, spacing: float = 0.1
) -> list[Pose3F64]:
    """Compute a straight segment of a square.

    Args:
        previous_pose (Pose3F64): The previous pose.
        distance (float): The side length of the square, in meters.
        spacing (float): The spacing between waypoints, in meters.

    Returns:
        Pose3F64: The poses of the straight segment.
    """
    # Create a container to store the track segment waypoints
    segment_poses: list[Pose3F64]

    # For tracking the number of segments and remaining angle
    first_segment = True
    remaining_distance: float = distance

    while remaining_distance > 0:
        # Compute the distance of the next segment
        segment_distance: float = min(remaining_distance, spacing)

        # Compute the next pose
        straight_segment: Pose3F64 = Pose3F64(
            a_from_b=Isometry3F64([segment_distance, 0, 0], Rotation3F64.Rz(0)),
        )
        if first_segment:
            segment_poses = [previous_pose * straight_segment]
            first_segment = False
        else:
            segment_poses.append(segment_poses[-1] * straight_segment)

        # Update the remaining angle
        remaining_distance -= segment_distance

    return segment_poses

def create_turn_segment(
    previous_pose: Pose3F64, angle: float, spacing: float = 0.1
) -> list[Pose3F64]:
    """Compute a turn segment of a square.

    Args:
        previous_pose (Pose3F64): The previous pose.
        next_frame_b (str): The name of the child frame of the next pose.
        angle (float): The angle to turn, in radians (+ left, - right).
        spacing (float): The spacing between waypoints, in radians.
    Returns:
        list[Pose3F64]: The poses of the turn segment.
    """
    # Create a container to store the track segment waypoints
    segment_poses: list[Pose3F64]

    # For tracking the number of segments and remaining angle
    first_segment = True
    remaining_angle: float = angle

    while abs(remaining_angle) > 0:
        # Compute the angle of the next segment
        segment_angle: float = np.copysign(min(np.abs(remaining_angle), spacing), angle)

        # Compute the next pose
        turn_segment: Pose3F64 = Pose3F64(
            a_from_b=Isometry3F64.Rz(segment_angle),
        )
        if first_segment:
            segment_poses = [previous_pose * turn_segment]
            first_segment = False
        else:
            segment_poses.append(segment_poses[-1] * turn_segment)

        # Update the counter and remaining angle
        counter += 1
        remaining_angle -= segment_angle

    return segment_poses