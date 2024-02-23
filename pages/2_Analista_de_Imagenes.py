import streamlit as st
from utils import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
matplotlib.use('tkagg')
from PIL import Image
import os
import tempfile


st.title(':robot_face: Analista de  Imágenes')
st.text('Experto en analizar imágenes como por ejemplo: gráficos')
# Display DataFrame
# Create a file uploader widget
uploaded_img = st.file_uploader("Selecciona una imágen para analizar", type=["jpg", "jpeg", "png", "bmp", "gif", "tiff"])
if uploaded_img is not None:
    file_details = {"FileName": uploaded_img.name, "FileType": uploaded_img.type, "FileSize": uploaded_img.size}
    st.write(file_details)

    temp_dir = tempfile.mkdtemp()
    # Guardar la imagen en la carpeta temporal
    with open(os.path.join(temp_dir, uploaded_img.name), "wb") as f:
        f.write(uploaded_img.read())
    # Obtener la ruta de archivo de la imagen guardada
    image_path = os.path.join(temp_dir, uploaded_img.name)
    print(f'image temp path: {image_path}')

# Display the uploaded image
if uploaded_img is not None:
    # You can use st.image to display the image
    col1, col2 = st.columns(2, gap='large')
    with col1:
        st.image(uploaded_img, caption='Imágen subida', use_column_width= "auto", width=0.3)
    with col2:
        st.header(':robot_face: Analista')
        try:
            response = analyze_image(image_path, model=gcp_model_vision)
            st.write(response)
        except Exception as e:
            st.write(e)



