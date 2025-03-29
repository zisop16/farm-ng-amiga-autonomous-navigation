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
import json
from pathlib import Path
from track_pb2 import Track  # Corrected imports to use Pose for waypoints
from pose_pb2 import Pose

def load_gps_data(file_path: Path) -> list:
    """Load GPS data from the given file path.

    Args:
        file_path (Path): The path to the file containing the GPS data.

    Returns:
        list: A list of GPS data entries, each containing latitude, longitude, and altitude.
    """
    gps_data = []

    # Ensure the file exists
    if not file_path.exists():
        print(f"Error: The file {file_path} does not exist.")
        return gps_data

    # Read the file and parse the data
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) == 3:
                try:
                    # Convert latitude, longitude, and altitude to floats
                    latitude, longitude, altitude = map(float, parts)
                    gps_data.append((latitude, longitude, altitude))
                except ValueError:
                    print(f"Error parsing line: {line.strip()}")

    return gps_data


def generate_track(gps_data: list, track_name: str) -> Track:
    """Generate a Track protobuf message from the GPS data.

    Args:
        gps_data (list): A list of GPS data tuples (latitude, longitude, altitude).
        track_name (str): The name of the track.

    Returns:
        Track: A protobuf message containing the track information.
    """
    track = Track()

    # Add waypoints to the track
    for latitude, longitude, altitude in gps_data:
        # Use Pose instead of TrackFollowerState for waypoints
        waypoint = Pose(latitude=latitude, longitude=longitude, altitude=altitude)
        track.waypoints.append(waypoint)

    return track

def main(track_name: str, output_dir: Path) -> None:
    """Process GPS data and generate a track file.

    Args:
        track_name (str): The name of the track to generate.
        output_dir (Path): The directory to save the track file.
    """
    # Define the path to the gps_data.txt file
    gps_data_file_path = Path("../gps_client/gps_data.txt")

    # Load GPS data from the file
    gps_data = load_gps_data(gps_data_file_path)

    # If no data was loaded, exit early
    if not gps_data:
        print("No valid GPS data found.")
        return

    # Generate the track
    track = generate_track(gps_data, track_name)

    # Define the track file path
    track_file_path = output_dir / f"{track_name}.json"

    # Convert the track to a dictionary and save as a JSON file
    track_data = {
        "waypoints": [
            {"latitude": wp.latitude, "longitude": wp.longitude, "altitude": wp.altitude} 
            for wp in track.waypoints
        ]
    }

    # Save the track data to a JSON file
    with open(track_file_path, 'w') as track_file:
        json.dump(track_data, track_file, indent=4)

    print(f"Track has been saved to {track_file_path}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="python track_record.py", description="Process GPS data and generate a track.")
    parser.add_argument("--track-name", type=str, required=True, help="Name of the track to generate.")
    parser.add_argument("--output-dir", type=Path, required=True, help="Directory to save the generated track file.")
    args = parser.parse_args()

    main(args.track_name, args.output_dir)

