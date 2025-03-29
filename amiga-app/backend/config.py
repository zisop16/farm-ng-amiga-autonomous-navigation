from farm_ng.core.event_client_manager import EventClientSubscriptionManager
import os
import json
from typing import Optional
import subprocess

# Path to the GPS logging script
SERVICE_CONFIG_PATH =  "./service_config.json"

# Directory where track JSON files are stored
TRACKS_DIR = "./tracks/"

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
