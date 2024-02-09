import os
from fastapi import FastAPI, WebSocket, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from typing import Annotated, Union
from dataclasses import dataclass, asdict
import base64
from io import BytesIO
from PIL import Image


from web.media_handler.services import media_form_depends_execute, MediaFormService
from web.media_handler.utils import save_file, process_image, format_data, save_binary
from web.media_handler.schemas import CarAttributes

# import socketio

from web.media_handler.routers import media_router

# Base app confs
app = FastAPI()

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

app.include_router(media_router)

@app.websocket("/stream")
async def websocket_endpoint(websocket: WebSocket, service: Annotated[MediaFormService, Depends(media_form_depends_execute)]):
    await websocket.accept()

    while True:
        file_base64 = await websocket.receive_text()
        url, filepath = await save_binary(file_base64, filename="test")
        result: Union[dict, tuple] = await process_image(filepath)
        if isinstance(result, tuple):
                car_attributes = format_data(result)
                if isinstance(car_attributes, CarAttributes):
                    data_dict = asdict(car_attributes)
                    await service.create(data_dict, url)
                    await websocket.send_text(data_dict.get("license_plate_number"))
                else:
                    await websocket.send_text("Invalid image size. Please higher image quality")
        else:
            await websocket.send_text("Something went wrong")

# Media files initialization
os.makedirs("web/media/", exist_ok=True)
app.mount("/media/", StaticFiles(directory="web/media"), name="media")
