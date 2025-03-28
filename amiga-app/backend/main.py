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

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import asyncio
from pathlib import Path

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

    if event_manager:
        asyncio.create_task(event_manager.update_subscriptions())

    yield  # Allows FastAPI to properly initialize
    print("Shutting down...")


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

    queue = Queue()
    oakManager = Process(target=startCameras, args=(queue,))

    # run the server
    uvicorn.run(app, host="0.0.0.0", port=args.port)  # noqa: S104
