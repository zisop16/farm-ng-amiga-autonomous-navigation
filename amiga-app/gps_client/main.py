"""Example of a GPS service client."""
# Copyright (c) farm-ng, inc.
#
# Licensed under the Amiga Development Kit License (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://github.com/farm-ng/amiga-dev-kit/blob/main/LICENSE
#
# Unless required by applicable law or agreed to in writing, software



from __future__ import annotations

import argparse
import asyncio
from pathlib import Path

from farm_ng.core.event_client import EventClient
from farm_ng.core.event_service_pb2 import EventServiceConfig
from farm_ng.core.events_file_reader import proto_from_json_file
from farm_ng.gps import gps_pb2


async def main(service_config_path: Path, output_file: Path, duration: int) -> None:
    """Run the gps service client to collect GPS data and save to a file.

    Args:
        service_config_path (Path): The path to the GPS service config.
        output_file (Path): The path to the file where GPS data will be written.
        duration (int): The duration (in seconds) for how long to collect data.
    """
    # Load the configuration from the service config file
    config: EventServiceConfig = proto_from_json_file(service_config_path, EventServiceConfig())

    # Create the EventClient to subscribe to GPS data
    event_client = EventClient(config)

    # Start the collection process and indicate the start
    print(f"Starting GPS data collection for {duration} seconds...")

    start_time = asyncio.get_event_loop().time()

    # Open the file for writing (will create the file if it doesn't exist)
    with open(output_file, 'a') as file:
        # Collect GPS data for the given duration
        async for event, msg in event_client.subscribe(config.subscriptions[0]):
            if isinstance(msg, gps_pb2.GpsFrame):
                # Print a message indicating that data is being collected
                print("Recording GPS data...")

                # Write the GPS data (latitude, longitude, altitude) to the file
                file.write(f"{msg.latitude},{msg.longitude},{msg.altitude}\n")

            # Stop after the specified duration
            if asyncio.get_event_loop().time() - start_time > duration:
                break

    print("GPS data collection finished.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="python gps_collect.py", description="Collect GPS data and save to file.")
    parser.add_argument("--service-config", type=Path, required=True, help="The GPS service config.")
    parser.add_argument("--output-file", type=Path, required=True, help="File to store collected GPS data.")
    parser.add_argument("--duration", type=int, default=10, help="Duration in seconds for GPS data collection.")
    args = parser.parse_args()

    asyncio.run(main(args.service_config, args.output_file, args.duration))

