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

recyclable_lille = ["plastic","glass","metal","paper","cardboard"]

villeneuve_papier = ['papier','cardboard']

villeneuve_plastique = ['plastic','glass','metal']

villeneuve_organique = ['organic']

def choice():
    option = st.selectbox(
        'Dans quelle ville résidez vous ?',
        ('Lille', "Villeneuve d'Ascq"))

    st.write('You selected:', option)
    if option== 'Lille':
        image_lille = Image.open('src/lille.jpg')
        st.image(image_lille)

    if option== "Villeneuve d'Ascq":
        image_villeneuve = Image.open('src/villeneuve_d_ascq.png')
        st.image(image_villeneuve)
    return option
    

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

def predict(uploaded_file, option):
    # load image
    file = {'file': (uploaded_file.name, open(uploaded_file.name, 'rb'))}

    # request API to make prediction 
    response = requests.post(
        f"{URL}/upload_file",
        files=file,
    )

    #remove image
    os.remove(f"{uploaded_file.name}")

    if option == 'Lille':
        if response.json()["label"] in recyclable_lille:
            st.write("recyclable", response.json()["label"])

        else:
            st.write("non recyclable", response.json()["label"])

    if option =="Villeneuve d'Ascq":
        if response.json()["label"] in villeneuve_papier:
            st.write("Compartiment papier", response.json()["label"])

        elif response.json()["label"] in villeneuve_plastique:
            st.write("Compartiment plastique / conserve / verre", response.json()["label"])

        elif response.json()["label"] in villeneuve_organique:
            st.write("Compartiment déchets organiques", response.json()["label"])

        else:
            st.write("Compartiment non recyclable", response.json()["label"])

    return response.json()

    
def main():
    st.title('Image upload demo')

    option_1 = choice()

    uploaded_file = get_image()

    result = st.button('Run on image')
    if result:
        pred = predict(uploaded_file, option_1)
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