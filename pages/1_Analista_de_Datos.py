import streamlit as st
from utils import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
matplotlib.use('tkagg')
from streamlit_extras.app_logo import add_logo

st.set_page_config(
    page_title="Data Analyst Testing",
    page_icon=":robot_face:",
    layout="wide",
)

add_logo("https://geti.cl/public/img/geti-header-logo.webp", height=10)
st.title(':robot_face: Analista de datos')
# Display DataFrame
st.subheader("DataFrame cargado:")
try:
    df = st.session_state.df
    st.dataframe(df)
except Exception as e:
    st.error(f'Error: {e}')

user_input = st.text_input("Que desea saber de la tabla?")
#st_callback = StreamlitCallbackHandler(st.container())
if user_input:
    with st.spinner('Pensando...'):
        response = pandas_agent_func(df, user_input, model='gpt', steps=True) #,callback=st_callback

    output_response = response['output']
    code_response = response['intermediate_steps'][-1][0].tool_input['query']
    print('test: \n')
    print(code_response)

    #col1, col2, col3 = st.columns(3, gap='large')
    #with col1:
    st.header(":robot_face: Pandas Agent")
    st.write(output_response) #output_response

    st.subheader("Captured Output:")
    if code_response.split()[0] == 'import':
        st.code(exec(code_response), language='python')
    elif code_response.startswith('df'):
        try:
            st.dataframe(eval(code_response))
        except Exception as e:
            st.code(exec(code_response), language='python')
    else:
        start_index1 = code_response.rfind('```python')
        start_index2 = code_response.rfind(') ```')
        parsed_code = code_response[start_index1+10:start_index2+1]
        st.code(exec(parsed_code), language='python')
