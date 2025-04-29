import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from multiprocessing import Process, Queue
import depthai as dai
from cameraBackend import oakService
from time import sleep
import signal
import os
from typing import List
from cameraBackend.camera import Camera
from cameraBackend.pointCloud import PointCloudFusion

cameras: List[Camera] = []
cameraIps = ["10.95.76.11", "10.95.76.12", "10.95.76.13"]
CAMERA_PORT = "5000"

# def startCameras():
#     processes = []
#     try:
#         for i in range(0, len(cameraIps)):
#             cameraPort = "5000"
#             process = Process(target=oakService.uploadService, args=(cameraIps[i], cameraPort))
#             processes.append(process)
#             process.start()
#             # sleep(5)
#
#         # Wait for all processes to finish
#         for process in processes:
#             process.join()
#     except KeyboardInterrupt:
#         for process in processes:
#             process.terminate()
#         for process in processes:
#             process.join()


def startCameras(queue=None):
    device_infos = dai.Device.getAllAvailableDevices()
    device_infos.sort(key=lambda x: x.name, reverse=True)  # Sort by ip
    print(device_infos)
    for device_info in device_infos:
        if device_info.name == "10.95.76.10":
            continue
        cameras.append(Camera(device_info, CAMERA_PORT))
        sleep(2)

    pointCloudFusion = PointCloudFusion(cameras)

    if queue != None:
        while True:
            msg = queue.get()
            if msg == "align_point_clouds":
                pointCloudFusion.align_point_clouds()
            elif msg == "reset_alignment":
                pointCloudFusion.reset_alignment()
            elif msg == "save_point_cloud":
                pointCloudFusion.update_fused_point_cloud()
                pointCloudFusion.save_point_cloud()


if __name__ == "__main__":
    q = Queue()
    startCameras(q)
