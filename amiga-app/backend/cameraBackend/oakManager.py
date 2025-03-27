from multiprocessing import Process
import oakService
from time import sleep

cameraIps = [
    "10.95.76.11",
    "10.95.76.12",
    "10.95.76.13"
]

def startCameras():
    processes = []
    try:
        for i in range(0, len(cameraIps)):
            cameraPort = "5000"
            process = Process(target=oakService.uploadService, args=(cameraIps[i], cameraPort))
            processes.append(process)
            process.start()
            # sleep(5)
        
        # Wait for all processes to finish
        for process in processes:
            process.join()
    except KeyboardInterrupt:
        for process in processes:
            process.terminate()
        for process in processes:
            process.join()

if __name__ == "__main__":
    startCameras()

