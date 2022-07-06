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
classes_to_fr = {'clothes':'Vêtement', 
                 'battery':'Pile ou batterie', 
                 'biological':'Déchet organique', 
                 'cardboard':'Carton', 
                 'glass':'Verre', 
                 'metal':'Métal', 
                 'paper':'Papier', 
                 'plastic':'Plastique', 
                 'trash':'Déchet non recyclable'}

recyclable_lille = ["plastic","glass","metal","paper","cardboard"]

montreuil_jaune = ['paper','cardboard','metal','plastic']

montreuil_verre = ['glass']


def plastic_advice():
    st.write("Les pots de yaourt ne sont, pour l'instant, pas recyclables dans toutes les communes francaises, de même pour les sacs plastiques.")
    with st.expander("Fun fact", expanded=False):
        st.write("Sur 10 ans, la consommation d’emballages plastiques a été multipliée par 10. La France s'est donné pour objectif que tout le plastique soit recyclable en 2025. La France ne recycle que 29 % de ses déchets plastiques mais veut rattraper son retard")
    img1 = Image.open("src/plastic.png") 
    st.image(img1, width=200) 

def organic_advice():
    st.write("Les déchets issus des végétaux sont compostables. Veuillez les mettre dans un composteur, un lombricomposteur ou un bokashi par exemple.")
    with st.expander("Fun fact", expanded=False):
        st.write("Pour faire un bon compost, il faut utiliser de la matière brune c'est à dire carbonique comme du carton, des branchage etc... et souvent aérer son compost(valable aussi pour le lombricompostable). Bokashi est un nom japonais qui signifie littéralement : matière organique bien fermentée.")
    img2 = Image.open("src/organic.png") 
    st.image(img2, width=200) 

def cardboard_advice():
    st.write("A déchirer et à mettre dans les bacs de recyclage dédiés ou en entier en décheterie ( Attention, le carton souillé ne se recycle pas ! )")
    with st.expander("Fun fact", expanded=False):
        st.write("64% du carton ondulé produit est recyclé. On peut réutiliser la matière jusqu’à huit fois, après quoi la fibre se dégrade.")
    img3 = Image.open("src/paper.png") 
    st.image(img3, width=200)
    
def paper_advice():
    img3 = Image.open("src/paper.png") 
    st.image(img3, width=200) 

def glass_advice():
    st.write("Pensez à enlever le bouchon des bouteilles en verre")
    with st.expander("Fun fact", expanded=False):
        st.write("Le verre mettrait 3 ou 4 millénaires à se décomposer dans la nature sans recyclage. Les produits en verre sont les seuls déchets 100% recyclables.")
    img4 = Image.open("src/glass.png") 
    st.image(img4, width=200) 

def battery_advice():
    st.write("Attention, les batteries sont à déposer en décheterie ou dans les bacs dédiés en magasin")
    with st.expander("Fun fact", expanded=False):
        st.write("226 000 tonnes de piles et de batteries ont été mises en vente dans l'Union européenne en 2017. C'est le poids de 22 tours Eiffel. Chaque année, on estime à environ 45% de ces déchets sont collectés pour être revalorisés. Le mercure d'une pile bouton usagée peut contaminer 400 litres d'eau ou un mètre cube de terre pendant 50 ans.")
    img5 = Image.open("src/piles.png") 
    st.image(img5, width=200) 

def clothes_advice():
    st.write("Si en bon état, à vendre, à donner ou à déposer dans les bennes de collectes : https://refashion.fr/citoyen/fr/point-dapport")
    with st.expander("Fun fact", expanded=False):
        st.write(" En France, plus de 600 000 tonnes de vêtements finissent à la poubelle chaque année, soit l’équivalent de 60 tours Eiffel.")
    img6 = Image.open("src/vetements.jpeg") 
    st.image(img6, width=200)

def metal_advice():
    st.write("S'il s'agit de conserves veuillez les mettres dans la poubelle des recyclables, s'il s'agit d'un gros objet la déchèterie sera plus adaptée.")
    

def choice():
    option = st.selectbox(
        'Selectionnez votre Fabrique',
        ('Fabrique de Lille', "Fabrique de Montreuil"))

    st.write('Bravo, la nature  vous remercie pour votre geste à la', option)
    if option== 'Fabrique de Lille':
        img = Image.open("src/fab_lille.jpg") 
        st.image(img, width=200) 
        image_lille = Image.open('src/lille.jpg')
        st.image(image_lille)

    if option== "Fabrique de Montreuil":
        imag_montreuil = Image.open('src/fab_montreuil.jpeg')
        st.image(imag_montreuil, width=200)
        image_montreuil = Image.open('src/montreuil.jpg')
        st.image(image_montreuil)
        
    return option
    
def mode():
    mode= st.radio("Comment souhaitez-vous utiliser l'application ?",("Utiliser une photo existante","Prendre une photo"))
    st.write("Conseil: Pour de meilleures performances, essayez d'avoir un fond uni et un seul déchet dans la photo.")
    return mode 

def load_image(img):
    img = Image.open(img)
    return img


def get_image(photo_mode):
    # get image
    if photo_mode == "Prendre une photo":
        uploaded_file = st.camera_input("Prendre une photo")
    else :
        uploaded_file = st.file_uploader(label='Utiliser une image existante')

    if uploaded_file:
        # file_details = {"Filename":uploaded_file.name,"FileType":uploaded_file.type,"FileSize":uploaded_file.size}
        # st.write(file_details)
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
    if option == 'Fabrique de Lille':
        if response.json()["label"] in recyclable_lille:
            if float(response.json()["confidence"]) > 50:
                st.success("Prédiction: "+classes_to_fr[response.json()["label"]]+" à "+response.json()["confidence"]+"%")
            else:
                st.error("Prédiction: "+classes_to_fr[response.json()["label"]]+" à "+response.json()["confidence"]+"%")
                
            if response.json()["label"] == 'plastic':
                plastic_advice()

            elif response.json()["label"] == 'cardboard':
                cardboard_advice()
            
            elif response.json()["label"] == 'paper':
                paper_advice()

            elif response.json()["label"] == 'metal':
                metal_advice()
            
            elif response.json()["label"] == 'battery':
                battery_advice()

            elif response.json()["label"] == 'glass':
                glass_advice()
        else:
            if float(response.json()["confidence"]) > 50:
                st.success("Prédiction: "+classes_to_fr[response.json()["label"]]+" à "+response.json()["confidence"]+"%")
            else:
                st.error("Prédiction: "+classes_to_fr[response.json()["label"]]+" à "+response.json()["confidence"]+"%")

            if response.json()["label"] == 'biological':
                organic_advice()

            elif response.json()["label"] == 'clothes':
                clothes_advice()

    # Consignes Montreuil 
    if option =="Fabrique de Montreuil":

        if response.json()["label"] in montreuil_jaune:
            if float(response.json()["confidence"]) > 50:
                st.success("Prédiction: "+classes_to_fr[response.json()["label"]]+" à "+response.json()["confidence"]+"%")
            else:
                st.error("Prédiction: "+classes_to_fr[response.json()["label"]]+" à "+response.json()["confidence"]+"%")

            st.write("Poubelle jaune")

            if response.json()["label"] == 'plastic':
                plastic_advice()

            elif response.json()["label"] == 'cardboard':
                cardboard_advice()

            elif response.json()["label"] == 'metal':
                metal_advice()

            elif response.json()["label"] == 'paper':
                paper_advice()


        elif response.json()["label"] in montreuil_verre:
            if float(response.json()["confidence"]) > 50:
                st.success("Prédiction: "+classes_to_fr[response.json()["label"]]+" à "+response.json()["confidence"]+"%")
            else:
                st.error("Prédiction: "+classes_to_fr[response.json()["label"]]+" à "+response.json()["confidence"]+"%")
                
            st.write("Poubelle verte", response.json()["label"])
            glass_advice()
        
        elif response.json()["label"] == 'biological':
                organic_advice()
                st.write("Pas de composteur? Mettre les végétaux acceptés dans les sacs biodégradables mis à disposition gratuitement (pas de sacs plastiques) et sans débordement pour permettre leur fermeture. Déposez vos déchets végétaux sur le domaine public la veille de la collecte à partir de 21h ou avant 6h le jour de la collecte.")
        else:
            if float(response.json()["confidence"]) > 50:
                st.success("Prédiction: "+classes_to_fr[response.json()["label"]]+" à "+response.json()["confidence"]+"%")
            else:
                st.error("Prédiction: "+classes_to_fr[response.json()["label"]]+" à "+response.json()["confidence"]+"%")
                
            st.write("Bac à ordures ménageres marron", response.json()["label"])
            if response.json()["label"] == 'clothes':
                clothes_advice()

    return response.json()


#Accueil
def main():
    img = Image.open("src/bin.png") 
    st.image(img) 
    st.title("L'appli qui t'aide à trier tes déchets..")
    
    option_1 = choice()

    photo_mode = mode()
    uploaded_file = get_image(photo_mode)

    result = st.button('Obtenir les consignes de Tri')
    if result:
        pred = predict(option_1)
        # st.write(pred)
        if float(pred['confidence']) < 50:
            st.write(f"L'indice de confiance étant inférieur à 50%, renseignez-vous un peu plus pour être sûr de la manière de trier ce type de déchet.")
        st.write("Si malgrés la prédiction vous avez un doute, veuillez déposer votre déchet dans la poubelle des non recyclables. Un déchet à la poubelle est mieux qu'un déchet dans la nature.")
    # st.write(" ")
    # st.write(" ")
    # img = Image.open("src/poub.png") 
    # st.image(img) 

if __name__ == '__main__':
    main()