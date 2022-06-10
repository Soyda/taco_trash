import uvicorn
from fastapi import FastAPI, File, Uploadfile

import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World to Scan'n'Sort API "}

@app.get("/prediction")
def predict():
    model = load_model("modele_alpha_mich")
    
    classes = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']

    path = "img_test.jpg"

    img = tf.keras.preprocessing.image.load_img(path, target_size=(256, 256))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0) 

    predictions = model.predict(img_array)

    return {"label":classes[np.argmax(predictions)] + f" {np.round(predictions[0][np.argmax(predictions)]*100, 2)}%",
            "bin":"TEST_BIN"}

@app.get("/{test}")
def test(test):
    test = test + " plop"
    return f"Hello {test}"

if __name__ == "__main__":
    uvicorn.run("main:app")