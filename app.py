import streamlit as st
import pandas as pd
import os
from langchain_community.callbacks import StreamlitCallbackHandler
from contextlib import redirect_stdout
from io import StringIO
from utils import *
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
matplotlib.use( 'tkagg' )

st.set_page_config(
    page_title="App LLMs Testing",
    page_icon=":robot_face:",
    layout="wide",
)

st.title(':robot_face: Testing Agents')

uploaded_file = st.file_uploader("Seleccione un archivo CSV", type="csv")

try:
    if uploaded_file is not None:
        file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type, } #"FileSize": uploaded_file.size
        st.write(file_details)

        with open("temp.csv", "wb") as f:
            f.write(uploaded_file.getvalue())

        temp_location = os.path.abspath("temp.csv")
        print(temp_location)

        #Dataframe formatting
        df = pd.read_csv(temp_location)
        df = format_compete_table(df)
        #df.to_csv('temp_preproc.csv')
        #temp_preproc_location = os.path.abspath("temp_preproc.csv")

        # Display DataFrame
        st.subheader("DataFrame cargado:")
        st.dataframe(df)

        user_input = st.text_input("Que desea saber de la tabla?")
        #st_callback = StreamlitCallbackHandler(st.container())
        agent_response = pandas_agent_func(df, user_input, model='gpt', steps=True) #,callback=st_callback
        output_response = agent_response['output']
        code_response = agent_response['intermediate_steps'][-1][0].tool_input['query']
        print('test: \n')
        print(code_response)

        #col1, col2, col3 = st.columns(3, gap='large')
        #with col1:
        st.header(":robot_face: Pandas Agent")
        st.write(output_response) #output_response
        #with StringIO() as output_buffer:
        #    with redirect_stdout(output_buffer):
        #        print(code_response.split()[0])
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
            #captured_output = output_buffer.getvalue(
        #st.subheader("Captured Output:")
        #st.code(captured_output, language='python')
            #st.subheader("Method used:")
            #st.write('\n'.join([step[0].tool_input for step in agent_response['intermediate_steps']]))#[0][0].tool_input
        #with col2:
        #    st.header(":robot_face: Agent")
        #    st.write('Agent 2: on hold')

except Exception as e:
    st.error(f"Error: {e}. Check your uploaded dataset")
