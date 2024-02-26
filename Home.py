import streamlit as st
import pandas as pd
import os
from utils import format_pricing_table, format_compete_table



st.set_page_config(
    page_title="App LLMs Testing",
    page_icon=":robot_face:",
    layout="wide",
)

st.title(':wrench: Dashboard & LLMs Tests :wrench:')

uploaded_file = st.file_uploader("Seleccione un archivo CSV para analizar", type="csv")

try:
    if uploaded_file:
        file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type, } #"FileSize": uploaded_file.size
        st.write(file_details)

        with open("temp.csv", "wb") as f:
            f.write(uploaded_file.getvalue())

        temp_location = os.path.abspath("temp.csv")

        #Dataframe formatting
        if 'df' not in st.session_state:
            df = pd.read_csv(temp_location)
            df = format_compete_table(df)

            # Save the data to session state
            st.session_state.df = df

        st.subheader("DataFrame Head:")
        st.dataframe(df.head(10))

        st.subheader("DataFrame Stats:")
        st.dataframe(df.describe())
except Exception as e:
    st.error(f"Error: {e}. Check your uploaded dataset")
