# import Part
from typing import Union

from fastapi import FastAPI
from fastapi.responses import FileResponse

# BackEnd Part
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/images/{image_id}")
async def get_image(image_id: str):
    image_path = "images/"+image_id+".PNG"
    return FileResponse(image_path)