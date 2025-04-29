# from farm_ng.core.event_client_manager import EventClientSubscriptionManager
import os
import json
from typing import Optional
import subprocess
from pydantic import BaseModel
from farm_ng_core_pybind import Isometry3F64
from farm_ng_core_pybind import Pose3F64
from farm_ng_core_pybind import Rotation3F64
import numpy as np


class StateVars(BaseModel):
    track_recording: bool = False
    # Name of the line being recorded, so it can be accessed
    line_recording: str = None
    # 2 dimensional vectors
    line_start: np.ndarray = None
    line_end: np.ndarray = None
    turn_calibrating: bool = False
    turn_calibration_start: Pose3F64 = None
    turn_calibration_segments: int = 0
    turn_length: float = 0
    following_track: bool = False

    class Config:
        arbitrary_types_allowed = True


# Path to the GPS logging script
SERVICE_CONFIG_PATH = "./service_config.json"

# Directory where track JSON files are stored
TRACKS_DIR = "./tracks/"
# Directory where line track JSON files are stored
LINES_DIR = "./lines/"

POINTCLOUD_DATA_DIR = "./pointcloud_data"

# Camera configs
CALIBRATION_DATA_DIR = "./calibration_data"
MIN_RANGE_MM = 100
MAX_RANGE_MM = 1000

# Global process handler for Nav Logger
# gps_logging_process: Optional[subprocess.Popen] = None


# Port
PORT = 8042
manifest_path = "./manifest.json"

with open(manifest_path, "r") as manifest_file:
    data = json.load(manifest_file)

for child_name, child_info in data["services"].items():
    app_route = child_info.get("app_route")
    if app_route:
        PORT = int(app_route)
