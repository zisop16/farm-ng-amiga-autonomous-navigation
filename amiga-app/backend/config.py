from farm_ng.core.event_client_manager import EventClientSubscriptionManager
import os
from typing import Optional
import subprocess

# Path to the GPS logging script
SERVICE_CONFIG_PATH = os.getcwd() + "../service_config.json"

# Directory where track JSON files are stored
TRACKS_DIR = os.getcwd() + "../tracks/"

# Global process handler for Nav Logger
gps_logging_process: Optional[subprocess.Popen] = None

# Declare event_manager globally to avoid "not initialized" errors
event_manager: Optional[EventClientSubscriptionManager] = None

# Port
PORT = 8042
