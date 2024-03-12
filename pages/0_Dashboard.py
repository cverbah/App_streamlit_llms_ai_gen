import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
matplotlib.use('tkagg')
from PIL import Image
import os
import streamlit as st
from streamlit_extras.app_logo import add_logo

st.set_page_config(
    page_title="Dashboard Testing",
    page_icon="	:gear:",
    layout="wide",
)
add_logo("https://www.python.org/static/community_logos/python-powered-w-100x40.png", height=1)
st.title('Dashboard: #Todo')
try:
    with st.spinner('Cargando datos...'):
        df = st.session_state.df

except Exception as e:
    st.error(e)

with st.sidebar:
    st.title('Dashboard')

    #state
    state = df['tipo_oferta'].unique().tolist()
    select_offer = st.selectbox('Seleccione el tipo de oferta', state, index=len(state) - 1)
    if select_offer:
        df_filtered = df[df.tipo_oferta == select_offer].reset_index(drop=True)

# Dashboard Main Panel
col1, col2, col3 = st.columns(3, gap='medium')
with col1:
    st.write('todo')

with col2:
    st.write('todo')

with col3:
    st.write('todo')


