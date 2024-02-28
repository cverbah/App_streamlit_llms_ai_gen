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
import time
from streamlit_extras.app_logo import add_logo

st.set_page_config(
    page_title="Images Analyst Testing 2",
    page_icon=":robot_face:",
    layout="wide",
)

add_logo("https://geti.cl/public/img/geti-header-logo.webp", height=10)
st.title(':robot_face: Analista de  Promociones')
st.text('Experto en extraer info de anuncios')

uploaded_img = st.file_uploader("Selecciona una imágen para analizar", type=["jpg", "jpeg", "png", "bmp", "gif", "webp"], key="1")
if uploaded_img:
    file_details = {"FileName": uploaded_img.name, "FileType": uploaded_img.type, "FileSize": uploaded_img.size}
    #st.write(file_details)

    # Save temp img
    temp_dir = tempfile.mkdtemp()
    with open(os.path.join(temp_dir, uploaded_img.name), "wb") as f:
        f.write(uploaded_img.read())

    image_path1 = os.path.join(temp_dir, uploaded_img.name)
    #print(f'image temp path: {image_path}')

uploaded_img2 = st.file_uploader("Selecciona una imágen para analizar", type=["jpg", "jpeg", "png", "bmp", "gif", "webp"], key="2")
if uploaded_img2:
    file_details = {"FileName": uploaded_img2.name, "FileType": uploaded_img2.type, "FileSize": uploaded_img2.size}
    # Save temp img
    temp_dir2 = tempfile.mkdtemp()
    with open(os.path.join(temp_dir2, uploaded_img2.name), "wb") as f:
        f.write(uploaded_img2.read())

    image_path2 = os.path.join(temp_dir2, uploaded_img2.name)

# Display the uploaded image
if uploaded_img:

    col1, col2, col3 = st.columns(3, gap='large')
    with col1:
        st.header(':frame_with_picture: Imagen 1')

        st.image(uploaded_img, caption='image', use_column_width='auto', width=0.8)

    with col2:
        st.header(':frame_with_picture: Imagen 2 ')
        time.sleep(3)
        st.write('Dummy')
        #st.image(uploaded_img2, caption='image2', use_column_width='auto', width=0.8)
    with col3:
        st.header(':robot_face: Analista Promos')
        try:
            with st.spinner('Pensando...'):
                #if uploaded_img2:
                image_path2 = 'dummy'
                response = analyze_promo_v2(image_path1, image_path2, model=gcp_model_vision)
                st.write(response)
                st.success('Ok!')

        except Exception as e:
            st.error(e)
