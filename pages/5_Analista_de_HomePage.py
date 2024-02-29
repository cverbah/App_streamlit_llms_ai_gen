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
st.title(':male-detective: Analista de  Páginas de Inicio')
st.text('..')

uploaded_img = st.file_uploader("Selecciona una imágen para analizar", type=["jpg", "jpeg", "png", "bmp", "gif", "webp"], key="3")
if uploaded_img:
    file_details = {"FileName": uploaded_img.name, "FileType": uploaded_img.type, "FileSize": uploaded_img.size}
    #st.write(file_details)

    # Save temp img
    temp_dir = tempfile.mkdtemp()
    with open(os.path.join(temp_dir, uploaded_img.name), "wb") as f:
        f.write(uploaded_img.read())

    image_path = os.path.join(temp_dir, uploaded_img.name)

    # Display the uploaded image
    if uploaded_img:

        col1, col2 = st.columns(2, gap='large')
        with col1:
            st.header(':frame_with_picture: Home Page Retail X')

            st.image(uploaded_img, caption='image', use_column_width='auto', width=0.8)

        with col2:
            st.header(':male_mage: El Mago')
            try:
                with st.spinner('Pensando...'):
                    st.write('todo')
                    st.success('Ok!')

            except Exception as e:
                st.error(e)