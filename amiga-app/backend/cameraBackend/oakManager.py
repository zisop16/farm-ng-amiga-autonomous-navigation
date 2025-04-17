import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import signal
from multiprocessing import Queue
import depthai as dai
from time import sleep
import os
from typing import List
from cameraBackend.camera import Camera
from cameraBackend.pointCloud import PointCloudFusion

# Last digit of ip identifies the camera
# 0 = Oak0, etc
cameras: List[Camera] = []
cameraIps = ["10.95.76.11", "10.95.76.12", "10.95.76.13"]
# STREAM_PORT_BASE + last 2 digits of ip identifies the port for streaming
STREAM_PORT_BASE = "50"

FPS = 30
STREAM_FPS = 10


def calibrate_cameras(cameras):
    # TODO: generate camera calibration
    pass


def startCameras(queue=None):
    device_infos = dai.Device.getAllAvailableDevices()
    device_infos.sort(key=lambda x: x.name, reverse=True)  # Sort by ip
    print(device_infos)
    for device_info in device_infos:
        if device_info.name == "10.95.76.10":
            continue  # Not using Oak0
        print(f"Initializing camera {device_info.name}")
        port = STREAM_PORT_BASE + device_info.name[-2:]
        cameras.append(Camera(device_info, port, FPS, STREAM_FPS))  # Initialize camera
        sleep(2)

    pointCloudFusion = PointCloudFusion(cameras)

    if queue != None:
        # Difference between calibration and alignment is that calibration
        # defines initial camera positioning and alignment refines the
        # positioning. Calibration requires calibration pattern and is
        # mandatory. Alignment is optional and can be done on the fly.
        actions = {
            "calibrate_cameras": calibrate_cameras,
            "align_point_clouds": pointCloudFusion.align_point_clouds,
            "reset_alignment": pointCloudFusion.reset_alignment,
            "save_point_cloud_snapshot": pointCloudFusion.save_point_cloud,
            # "start_point_cloud_continuous": pointCloudFusion.save_point_cloud,
            # "stop_point_cloud_continuous": pointCloudFusion.save_point_cloud,
        }
        while True:
            msg = queue.get()  # Blocking

            if msg == "shutdown":
                # TODO: check if this is all that's needed to shutdown cameras properly
                for camera in cameras:
                    camera.__del__()
                return

            action = actions.get(msg, None)
            if action:
                action()
                continue
            else:
                print(f"Unknown message: {msg}")

def handle_sigterm(signum, frame):
    print("Received SIGTERM, stopping oak manager")
    for camera in cameras:
        camera.__del__()
    sys.exit(0)
signal.signal(signal.SIGTERM, handle_sigterm)



if __name__ == "__main__":
    q = Queue()
    startCameras(q)
