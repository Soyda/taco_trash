import streamlit as st
import tensorflow as tf
from tensorflow import keras
from PIL import Image
import io
import os
import numpy as np
import requests



URL = "http://host.docker.internal:8000"

classes = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']

recyclable_lille = ["plastic","glass","metal","paper"]

def load_model():
    model = keras.models.load_model('modele_alpha_mich')
    return model

    

# fonction test
def load_image(img):
    img = Image.open(img)
    return img


def get_image():
    # get image
    uploaded_file = st.file_uploader(label='Pick an image to test')

    if uploaded_file:
        file_details = {"Filename":uploaded_file.name,"FileType":uploaded_file.type,"FileSize":uploaded_file.size}
        st.write(file_details)
        img = load_image(uploaded_file)
        st.image(img)

        # save image
        with open(uploaded_file.name,"wb") as f:
            f.write(uploaded_file.getbuffer())

    return uploaded_file

def predict(uploaded_file): #(model, image):
    # load image
    file = {'file': (uploaded_file.name, open(uploaded_file.name, 'rb'))}

    # request API to make prediction 
    response = requests.post(
        f"{URL}/upload_file",
        files=file,
    )

    #remove image
    os.remove(f"{uploaded_file.name}")

    return response.json()

    
def main():
    st.title('Image upload demo')

    uploaded_file = get_image()

    result = st.button('Run on image')
    if result:
        pred = predict(uploaded_file)
        st.write(pred)
    
#==============================================

    # # get image
    # uploaded_file = st.file_uploader(label='Pick an image to test')
    # file_details = {"Filename":uploaded_file.name,"FileType":uploaded_file.type,"FileSize":uploaded_file.size}
    # st.write(file_details)
    # img = load_image(uploaded_file)
    # st.image(img)

    # # save image
    # with open(uploaded_file.name,"wb") as f:
    #     f.write(uploaded_file.getbuffer())

    # # load image
    # file = {'file': (uploaded_file.name, open(uploaded_file.name, 'rb'))}

    # # request API to make prediction 
    # response = requests.post(
    #     f"{URL}/upload_file",
    #     files=file,
    # )

    # #remove image
    # os.remove(f"{uploaded_file.name}")

    # st.write(response.json())

#================================================
#================================================

    



if __name__ == '__main__':
    main()