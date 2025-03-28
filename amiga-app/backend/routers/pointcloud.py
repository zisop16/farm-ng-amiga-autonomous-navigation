from fastapi import APIRouter, Depends
from fastapi import HTTPException
import json
from pathlib import Path
from multiprocessing import Queue

from backend.config import *

router = APIRouter()

def get_message_queue():
    from main import queue
    return queue

@router.get("/pointcloud/save")
async def pointcloud_save(queue: Queue = Depends(get_message_queue)):
    """Save pointcloud to pointcloud_data_dir"""
    if not os.path.exists(POINTCLOUD_DATA_DIR):
        return {"message": "No point cloud directory found."}

    queue.put("save_point_cloud")

    return {"status": "Point cloud saved"}

@router.get("/pointcloud/align")
async def pointcloud_align(queue: Queue = Depends(get_message_queue)):
    """Create alignment config for cameras"""
    if not os.path.exists(CALIBRATION_DATA_DIR):
        return {"message": "No calibration data directory found."}

    queue.put("align_point_clouds")

    return {"status": "Camera alignment set"}

@router.get("/pointcloud/reset")
async def pointcloud_reset(queue: Queue = Depends(get_message_queue)):
    """Reset alignment of cameras"""
    if not os.path.exists(CALIBRATION_DATA_DIR):
        return {"message": "no calibration data directory found."}

    queue.put("reset_alignment")

    return {"status": "Camera alignment reset"}
