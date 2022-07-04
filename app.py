import streamlit as st
import tensorflow as tf
from tensorflow import keras
from PIL import Image
import io
import os
import numpy as np
import requests



URL = "https://fast-scrubland-37630.herokuapp.com"

# classes = ['clothes', 'battery', 'organic', 'cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']

recyclable_lille = ["plastic","glass","metal","paper","cardboard"]

montreuil_jaune = ['paper','cardboard','metal','plastic']

montreuil_verre = ['glass']


def plastic_advice():
    st.write("Les pots de yaourt sont pour l'instant pas recyclables dans toutes les communes francaises, de même pour les sacs plastiques.")

def organic_advice():
    st.write("Les déchets de végétaux sont compostables. A mettre dans un composteur, un lombricomposteur ou un bokashi par exemple.")

def cardboard_advice():
    st.write("La carton souillé ne se recycle pas. A déchirer pour mettre dans les bacs de recyclage dédiés ou entier à la décheterie")

def glass_advice():
    st.write("Pensez à enlever le bouchon des bouteilles en verre")

def battery_advice():
    st.write("Attention, les batteries sont à déposer en décheterie ou dans les bacs dédiés en magasin")

def clothes_advice():
    st.write("Si en bon état, à vendre ou donner ou à déposer dans les bennes de collectes : https://refashion.fr/citoyen/fr/point-dapport?")

def choice():
    option = st.selectbox(
        'Dans quelle ville résidez vous ?',
        ('Lille', "Montreuil"))

    st.write('You selected:', option)
    if option== 'Lille':
        image_lille = Image.open('src/lille.jpg')
        st.image(image_lille)

    if option== "Montreuil":
        image_montreuil = Image.open('src/montreuil.jpg')
        st.image(image_montreuil)
        
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
        
        # resize image
        image = Image.open(uploaded_file.name)
        image = image.resize((500,500),Image.ANTIALIAS)
        image.save(fp="newimage.png")

    return uploaded_file

def predict(option):
    # load image
    file = {'file': ("newimage.png", open("newimage.png", 'rb'))}

    # request API to make prediction 
    response = requests.post(
        f"{URL}/upload_file",
        files=file,
    )

    #remove images in directory
    # os.remove(f"{uploaded_file.name}")
    for file in os.listdir() :
        if file.endswith(('.png', ".jpg", ".jpeg")):
            os.remove(file) 
    # Consignes Lille


    if option == 'Lille':
        if response.json()["label"] in recyclable_lille:
            
            st.write("recyclable", response.json()["label"])

            if response.json()["label"] == 'plastic':
                plastic_advice()

            elif response.json()["label"] == 'cardboard':
                cardboard_advice()

            elif response.json()["label"] == 'metal':
                battery_advice()


            elif response.json()["label"] == 'glass':
                glass_advice()
        else:
            st.write("non recyclable", response.json()["label"])


    # Consignes Montreuil 


    if option =="Montreuil":

        if response.json()["label"] in montreuil_jaune:

            st.write("Poubelle jaune", response.json()["label"])

            if response.json()["label"] == 'plastic':
                plastic_advice()

            elif response.json()["label"] == 'cardboard':
                cardboard_advice()

            elif response.json()["label"] == 'metal':
                battery_advice



        elif response.json()["label"] in montreuil_verre:

            st.write("Poubelle verte", response.json()["label"])

            glass_advice()

        else:
            st.write("Bac à ordures ménageres marron", response.json()["label"])

    return response.json()

    
def main():
    st.title('Image upload demo')

    option_1 = choice()

    uploaded_file = get_image()

    result = st.button('Run on image')
    if result:
        pred = predict(option_1)
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