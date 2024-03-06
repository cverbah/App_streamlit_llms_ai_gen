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
add_logo("https://images.datacamp.com/image/upload/v1640050215/image27_frqkzv.png", height=10)
st.title('Dashboard: #Todo')
try:
    with st.spinner('Cargando datos...'):
        df = st.session_state.df

except Exception as e:
    st.error(e)

with st.sidebar:
    st.title('Dashboard')

    #state
    state = df['estado'].unique().tolist()
    select_state = st.selectbox('Seleccione estado', state, index=len(state) - 1)
    if select_state:
        df_filtered = df[df.estado == select_state].reset_index(drop=True)

# Dashboard Main Panel
col1, col2, col3 = st.columns(3, gap='medium')
with col1:
    st.write('todo')

with col2:
    st.write('todo')

with col3:
    st.write('todo')


