import uvicorn
from fastapi import FastAPI, File, UploadFile

import os
import pathlib

import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
from io import BytesIO

app = FastAPI()

model = load_model("modele_alpha_mich")
# model = load_model("modele_nounou_1_087")


@app.get("/")
async def root():
    return {"message": "Welcome to Scan'n'Sort API "}



@app.post("/upload_file")
async def read_root(file: UploadFile = File()):
 
    image = file.file._file

    #classes 
    classes = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']
    # classes = ['clothes', 'battery', 'organic', 'cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']

    recyclable_lille = ["plastic","glass","metal","paper","cardboard"]

    #PREPROCESSING AND PREDICTION
    img = tf.keras.preprocessing.image.load_img(image, target_size=(256, 256))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0) 

    predictions = model.predict(img_array)

    if classes[np.argmax(predictions)] in recyclable_lille:
        bin = "recyclable"
    else :
        bin = "not recyclable"


    return {"info": f"file '{file.filename}'",
            "label":classes[np.argmax(predictions)],
            "confidence": f"{np.round(predictions[0][np.argmax(predictions)]*100, 2)}%",
            "bin":bin}


if __name__ == "__main__":
    uvicorn.run("main:app")