!pip install fastapi nest-asyncio pyngrok uvicorn
!pip install pyngrok
!pip install streamlit -q
!pip install deepface
!pip install python-multipart
!pip install opencv-python

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from deepface import DeepFace
import json
import tempfile
import base64
import numpy as np
from io import BytesIO
from PIL import Image
import cv2

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

class ImageComparisonRequest(BaseModel):
    image1_base64: str
    image2_base64: str


def decode_base64_image(base64_string: str) -> np.ndarray:
    # Decode base64 string to bytes and load it as an image using PIL, then convert to numpy array
    try:
        image_data = base64.b64decode(base64_string)
        #image = Image.open(BytesIO(image_data))
        #nparr = np.frombuffer(image_data, np.uint8)
        #img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_img_file:
            temp_img_file.write(image_data)
            temp_img_path = temp_img_file.name
            return temp_img_path

        return None
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid base64 image data")

@app.post("/compare_faces")
async def compare_faces(request: ImageComparisonRequest):
    # Decode both images from base64
    try:
        img1 = decode_base64_image(request.image1_base64)
        img2 = decode_base64_image(request.image2_base64)
    except HTTPException as e:
        return {"error": str(e.detail)}

    try:
        # Perform face comparison using DeepFace
        result = DeepFace.verify(img1, img2, threshold=0.6, enforce_detection=True, align=True, normalization="base")
        print(result)
        return result
    except Exception as e:
        return {"error": f"Exception while processing images: {str(e)}"}


@app.get("/")
async def root():
    return {"message": "Face comparison API is running"}
