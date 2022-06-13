import streamlit as st
from tensorflow import keras
import requests


# model = keras.models.load_model(r'C:\Users\sofia\Downloads\modele_nounou')

URL = "http://host.docker.internal:8000"

def load_image():
    uploaded_file = st.file_uploader(label='Pick an image to test')
    if uploaded_file is not None:
        image_data = uploaded_file.getvalue()
        st.image(image_data)
        
    st.button('Predict')
    
    # if st.button:
    #     prediction = model.predict(uploaded_file)
    #     st.write(prediction)

    
def main():
    st.title('Image upload demo')
    x = requests.get('http://host.docker.internal:8000/')
    st.write(x.json()["message"])
    load_image()


if __name__ == '__main__':
    main()
    
    


