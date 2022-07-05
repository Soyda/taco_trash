import streamlit as st
import tensorflow as tf
from tensorflow import keras
from PIL import Image
import io
import os
import numpy as np
import requests



# URL = "https://fast-scrubland-37630.herokuapp.com"
URL = "http://host.docker.internal:8000"

# classes = ['clothes', 'battery', 'organic', 'cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']

recyclable_lille = ["plastic","glass","metal","paper","cardboard"]

montreuil_jaune = ['paper','cardboard','metal','plastic']

montreuil_verre = ['glass']


def plastic_advice():
    st.write("Les pots de yaourt sont pour l'instant pas recyclables dans toutes les communes francaises, de même pour les sacs plastiques.")

def organic_advice():
    st.write("Les déchets de végétaux sont compostables. A mettre dans un composteur, un lombricomposteur ou un bokashi par exemple.")

def cardboard_advice():
    st.write("Le carton souillé ne se recycle pas. A déchirer pour mettre dans les bacs de recyclage dédiés ou entier à la décheterie")

def glass_advice():
    st.write("Pensez à enlever le bouchon des bouteilles en verre")

def battery_advice():
    st.write("Attention, les batteries sont à déposer en décheterie ou dans les bacs dédiés en magasin")

def clothes_advice():
    st.write("Si en bon état, à vendre ou donner ou à déposer dans les bennes de collectes : https://refashion.fr/citoyen/fr/point-dapport?")

def choice():
    option = st.selectbox(
        'Selectionnez votre Fabrique',
        ('Fabrique de Lille', "Fabrique de Montreuil"))

    st.write('Fabrique de', option)
    if option== 'Fabrique de Lille':
        img = Image.open("src/fab_lille.jpg") 
        st.image(img, width=700) 
        image_lille = Image.open('src/lille.jpg')
        st.image(image_lille, width=700)

    if option== "Fabrique de Montreuil":
        image_montreuil = Image.open('src/montreuil.jpg')
        st.image(image_montreuil)
        
    return option
    
def mode():
    mode= st.radio("Comment voulez vous utiliser l'application ?",("Utiliser une photo existante","Prendre une photo"))
    return mode 

def load_image(img):
    img = Image.open(img)
    return img


def get_image(photo_mode):
    # get image
<<<<<<< HEAD
    uploaded_file = st.file_uploader(label='Montre nous ton déchet')
=======
    if photo_mode == "Prendre une photo":
        uploaded_file = st.camera_input("Prendre une photo")
    else :
        uploaded_file = st.file_uploader(label='Utiliser une image existante')
>>>>>>> eb547c3102c50eddc66189c7dfdd2c903c664281

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
        if file.endswith(('.png', ".jpg", ".jpeg", ".webp")):
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

            # elif response.json()["label"] == 'metal':
            #     paper_advice()

            # elif response.json()["label"] == 'paper':
            #     paper_advice()


        elif response.json()["label"] in montreuil_verre:

            st.write("Poubelle verte", response.json()["label"])

            glass_advice()

        else:
            st.write("Bac à ordures ménageres marron", response.json()["label"])

    return response.json()


#Accueil
    
def main():
    img = Image.open("src/simplon.png") 
    st.image(img, width=700) 
    st.title("What'S The Bin !?")
    "L'appli qui t'aide à trier tes déchets.."
    option_1 = choice()

<<<<<<< HEAD

    uploaded_file = get_image()
=======
    photo_mode = mode()
    uploaded_file = get_image(photo_mode)
>>>>>>> eb547c3102c50eddc66189c7dfdd2c903c664281

    result = st.button('Obtenir les consignes de Tri')
    if result:
        pred = predict(option_1)
        st.write(pred)
    

if __name__ == '__main__':
    main()