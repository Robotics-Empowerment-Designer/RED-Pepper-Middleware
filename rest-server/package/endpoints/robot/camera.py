import os

import numpy as np
from flask import Response, request
from ...server import app, socketio
from ...pepper.connection import camera
from ...pepper.connection import memory
from ...pepper.connection import sonar
from ...pepper.connection import tts
from ...pepper.connection import audio
from ...pepper.connection import tablet

from PIL import Image
import base64


@app.route("/pepper/camera")
def get_camera_pic():

    # Retrieve camera index and encoding parameters from the request
    camera_index = request.args.get("cameraIndex", default=0, type=int)
    encoding = request.args.get("encoding", default="base64", type=str)

    # Initialize the video service and set parameters
    video_service = camera
    fps = 5 # Frames per second
    resolution = 2 # VGA resolution
    colorSpace = 11 # RGB color space

    # Subscribe to the video service to get the camera feed
    videoClient = video_service.subscribe("python_client", resolution, colorSpace, fps)

    # Get a single frame from the camera feed
    img = video_service.getImageRemote(videoClient)
    image_width = img[0]
    image_height = img[1]
    image_array = img[6]

    # Create an image object from the raw data
    im = Image.frombytes("RGB", (image_width, image_height), image_array, 'raw')

    # Save the image.
    im.save("/home/img/camImage.png", "PNG")

    # Unsubscribe from the video service
    video_service.unsubscribe(videoClient)

    # If encoding is "raw", return the raw image data
    if encoding == "raw":
        raw_data = img[6]
        return Response(raw_data, status=200, mimetype='application/octet-stream')
    
    # Open the saved image file and encode it to base64
    with open("/home/img/camImage.png", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())

    return Response(str(encoded_string.decode('utf-8')), status=200)
