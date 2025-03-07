import csv
import sys
import os
import time

def playback_route(route_number):
    """Reads a recorded route from CSV and replays the ECEF coordinates."""
    file_path = f"route_{route_number}.csv"
    
    if not os.path.exists(file_path):
        print(f"Route {route_number} does not exist.")
        return
    
    print(f"Replaying Route {route_number}...\n")
    
    with open(file_path, "r") as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header
        
        for row in csv_reader:
            x, y, z = row
            print(f"ECEF: X={x}, Y={y}, Z={z}")
            time.sleep(0.5)  # Simulates playback delay

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python playback.py <route_number>")
        sys.exit(1)
    
    route_number = sys.argv[1]
    
    if not route_number.isdigit():
        print("Error: Route number must be a valid integer.")
        sys.exit(1)
    
    playback_route(int(route_number))
