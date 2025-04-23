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

import signal
import sys
import os
from pathlib import Path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Navigate one directory out of the location of main.py
os.chdir(f"{Path(__file__).parent}/..")

import asyncio


import uvicorn
from farm_ng.core.event_client_manager import EventClientSubscriptionManager
from farm_ng.core.event_service_pb2 import EventServiceConfigList
from farm_ng.core.events_file_reader import proto_from_json_file

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from multiprocessing import Process, Queue

from config import *

from routers import tracks, record, follow

from cameraBackend.oakManager import startCameras


@asynccontextmanager
async def lifespan(app: FastAPI):
    global event_manager
    print("Initializing App...")

    # config with all the configs
    base_config_list: EventServiceConfigList = proto_from_json_file(
        args.config, EventServiceConfigList()
    )

    # filter out services to pass to the events client manager
    service_config_list = EventServiceConfigList()
    for config in base_config_list.configs:
        if config.port == 0:
            continue
        service_config_list.configs.append(config)

    event_manager = EventClientSubscriptionManager(config_list=service_config_list)

    global queue
    queue = Queue()
    global oak_manager
    oak_manager = Process(target=startCameras, args=(queue,))
    oak_manager.start()
    print(f"Starting oak manager with PID {oak_manager.pid}")
    
    asyncio.create_task(event_manager.update_subscriptions())

    yield {
        "event_manager": event_manager,
        "oak_manager": oak_manager
    } 

    print("Stopping camera services...")
    # Shutdown cameras properly
    oak_manager.terminate()
    oak_manager.join()



app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(tracks.router)
app.include_router(record.router)
app.include_router(follow.router)

    
def handle_sigterm(signum, frame):
    print("Received SIGTERM, stopping camera services")
    oak_manager.terminate()
    oak_manager.join(timeout=5)

    if oak_manager.is_alive():
        oak_manager.kill()
        oak_manager.join()
    sys.exit(0)
signal.signal(signal.SIGTERM, handle_sigterm)


if __name__ == "__main__":

    class Arguments:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

    args = Arguments(config="/opt/farmng/config.json", port=PORT, debug=False)

    # NOTE: we only serve the react app in debug mode
    if not args.debug:
        react_build_directory = Path(__file__).parent / ".." / "ts" / "dist"

        app.mount(
            "/",
            StaticFiles(directory=str(react_build_directory.resolve()), html=True),
        )
    
    # print(f"camera PID: {oakManager.pid}")

    # run the server
    uvicorn.run(app, host="0.0.0.0", port=args.port)  # noqa: S104
