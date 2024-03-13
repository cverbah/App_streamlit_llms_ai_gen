import pandas as pd
import numpy as np
import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
import os
import streamlit as st
from streamlit_extras.app_logo import add_logo
from utils_plots import plot_wordcloud, plot_against_offer_type
from streamlit_carousel import carousel

st.set_page_config(
    page_title="Dashboard Testing",
    page_icon="	:gear:",
    layout="wide",
)
add_logo("https://www.python.org/static/community_logos/python-powered-w-100x40.png", height=1)
st.title(':construction: Dashboard: :construction:')
try:
    with st.spinner('Cargando datos...'):
        df = st.session_state.df
        df_datetime = df.loc[0, 'datetime_checked']
        df_datetime = df_datetime.strftime("%d-%m-%Y")

except Exception as e:
    st.error(e)

with st.sidebar:
    st.title('Dashboard')

    offer_type = df['tipo_oferta'].unique().tolist()
    offer_type.extend(['todas'])
    select_offer = st.selectbox('Seleccione el tipo de oferta', offer_type, index=len(offer_type) - 1)
    if select_offer:
        if select_offer != 'todas':
            df_filtered = df[df.tipo_oferta == select_offer].reset_index(drop=True)

            df_filtered.drop(columns=['datetime_checked'], inplace=True)
        else:
            df_filtered = df
try:
    # Dashboard Main Panel
    col1, col2 = st.columns((0.2, 0.8), gap='small')
    with col1:
        st.subheader('Fecha extracción:')
        st.write(df_datetime, )
    with col2:
        with st.spinner('Cargando datos...'):
            items_carousel = [dict(title='', text=desc, img=img) for name, desc, img in
                              list(zip(df_filtered['nombre_promocion'].tolist(), df_filtered['descripcion_promo'].tolist(), df_filtered['url_img'].tolist()))]
            items_carousel[0]['interval'] = None
            carousel(items=items_carousel, width=1, height=200)


        st.subheader("DataFrame Filtrado:")
        st.dataframe(df_filtered)

    col_types = ['categorias_en_promo', 'marcas_en_promo', 'publico_objetivo']
    df_col = st.selectbox('Seleccione columna', col_types, index=len(col_types) - 1)
    col3, col4 = st.columns(2, gap='medium')
    with col3:
        with st.spinner('Cargando gráficos...'):
            st.subheader('Word Clouds')
            fig = plot_wordcloud(df_filtered, df_col, color='white', max_words=20)
            st.pyplot(fig)

    with col4:
        with st.spinner('Cargando gráficos...'):
            st.subheader(f'Cuenta de: {df_col}')
            fig = plot_against_offer_type(df_filtered, df_col, top=10)
            st.plotly_chart(fig, theme="streamlit")

except Exception as e:
    st.error(e)
