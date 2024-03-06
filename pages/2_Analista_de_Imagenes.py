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
    page_title="Images Analyst Testing",
    page_icon=":robot_face:",
    layout="wide",
)

add_logo("https://www.python.org/static/community_logos/python-powered-w-100x40.png", height=1)
st.title(':robot_face: Analista de  Imágenes')
st.text('Experto en analizar todo tipo de imágenes')

uploaded_img = st.file_uploader("Selecciona una imágen para analizar", type=["jpg", "jpeg", "png", "bmp", "gif", "webp"])
if uploaded_img is not None:
    file_details = {"FileName": uploaded_img.name, "FileType": uploaded_img.type, "FileSize": uploaded_img.size}
    #st.write(file_details)

    # Save temp img
    temp_dir = tempfile.mkdtemp()
    with open(os.path.join(temp_dir, uploaded_img.name), "wb") as f:
        f.write(uploaded_img.read())

    image_path = os.path.join(temp_dir, uploaded_img.name)
    #print(f'image temp path: {image_path}')

# Display the uploaded image
if uploaded_img:

    col1, col2 = st.columns(2, gap='large')
    with col1:
        st.header(':frame_with_picture: Imagen')

        st.image(uploaded_img, caption='image', use_column_width='auto',width=0.7)
    with col2:
        st.header(':robot_face: Analista 1')
        try:
            with st.spinner('Pensando...'):
                response = analyze_image(image_path, model=gcp_model_vision, analyst_type=1)
                st.write(response)
                st.success('Ok!')

            st.header(':robot_face: Analista Experto 2')
            with st.spinner('Pensando...'):
                response = analyze_image(image_path, model=gcp_model_vision, analyst_type=2)
                st.write(response)
                st.success('Ok!')

            st.header(':robot_face: Data Extractor:')
            with st.spinner('Pensando...'):
                response = analyze_image(image_path, model=gcp_model_vision, analyst_type=3)
                st.write(response)
                st.success('Ok!')

        except Exception as e:
            st.error(e)



