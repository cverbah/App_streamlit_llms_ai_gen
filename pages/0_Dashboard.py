import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
matplotlib.use('tkagg')
from PIL import Image
import os
import streamlit as st


st.set_page_config(
    page_title="Dashboard Testing",
    page_icon="	:gear:",
    layout="wide",
)
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
col1, col2, col3  = st.columns(3, gap='medium')
with col1:
    pass

with col2:
    pass

with col3:
    pass


