import os
import pandas as pd
import matplotlib.pyplot as plt
from contextlib import redirect_stdout
from io import StringIO
import streamlit as st
import numpy as np
from utils import *

## App ##
st.set_page_config(page_title='LLMs Test', page_icon=':boxing_glove:', layout="wide")
# Streamlit App
st.title(":boxing_glove: GPT-4 vs Gemini Pro :boxing_glove:")

# File Upload
uploaded_file = st.file_uploader("Upload CSV/Excel file", type=["csv", "xlsx"])
try:
    #processing file
    if uploaded_file is not None:
        # Check if the file exists
        #if not os.path.isfile(uploaded_file.name):
        #    st.error(f"Error: File '{uploaded_file.name}' does not exist.")
        #    st.stop()
        try:
            # Read uploaded file into a DataFrame
            df = pd.read_csv(uploaded_file)

        except Exception as e:
            st.error(f"Error: {e}. Check your uploaded dataset")

        # cooking
        df_to_analyze = df.iloc[:, :9].sample(15, random_state=111)
        df_to_analyze.columns = (df_to_analyze.columns.
                                 str.replace(' ', '_').
                                 str.lower().
                                 str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8'))

        df_to_analyze['sku'] = df_to_analyze['sku'].astype(str)
        df_to_analyze['mas_bajo'] = df_to_analyze['mas_bajo'].apply(lambda row: int(row.replace('$ ', '').replace(',', '')))
        df_to_analyze['mas_alto'] = df_to_analyze['mas_alto'].apply(lambda row: int(row.replace('$ ', '').replace(',', '')))
        df_to_analyze['precio_mercado'] = df_to_analyze['precio_mercado'].apply(lambda row: int(row.replace('$ ', '').replace(',', '')))
        df_to_analyze['precio_de_lista'] = df_to_analyze['precio_de_lista'].apply(lambda row: int(row.replace('$ ', '').replace(',', '')))


        # Display top 10 rows of the DataFrame
        st.subheader("DataFrame de prueba (15):")
        st.write(df_to_analyze)

        # User Input
        user_input = st.text_input("Que desea saber de la tabla?")
        #open_ai_response = openai_response(prompt=user_input, df=df_to_analyze, model=openai_model) ##HODDL
        gcp_response_v1 = gcp_response_v1(prompt=user_input, df=df_to_analyze, model=gcp_model_v1) #old
        gcp_response = gcp_response(prompt=user_input, df=df_to_analyze, model=gcp_model)  # old

        col1, col2, col3 = st.columns(3, gap='large')
        with col1:
            #st.header(":robot_face: Analista GPT-4")
            #st.write('on Hold') #open_ai_response
            st.header(":robot_face: Analista Gemini	:parrot:")
            st.write(gcp_response) #open_ai_response

        with col2:
            st.header(":robot_face: Analista Gemini")
            st.write(gcp_response_v1)

        with col3:
            st.header(":robot_face: Analista GPT-4")
            st.write('ON HOLD') #open_ai_response)

        #st.subheader("Respuesta GPT-4")
        #st.write(open_ai_response)

        #st.subheader("Respuesta Gemini Pro")
        #st.write(gcp_response)

        # PARA EJECUTAR CODIGO PYTHON CUANDO VIENE EN EL TEMPLATE
        #start_index1 = open_ai_response.find('#')
        #start_index2 = open_ai_response.rfind(')')
        #exec_code = open_ai_response[start_index1:start_index2 + 1]
        #with StringIO() as output_buffer:
        #    with redirect_stdout(output_buffer):
        #        exec(exec_code)
        #    captured_output = output_buffer.getvalue()
        #st.subheader("Captured Output:")
        #st.code(captured_output, language='python')


except Exception as e:
    st.error(f"Error: {e}")

import os
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
import json
import re
import matplotlib.pyplot as plt
import vertexai
import google.generativeai as genai
from langchain_openai import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_google_vertexai import VertexAI
from langchain_core.prompts import PromptTemplate

from langchain_experimental.agents import create_csv_agent
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain.agents.agent_types import AgentType


def csv_agent_func(file_path, user_message, callback):
    """Run the CSV agent with the given file path and user message."""
    try:
        agent = create_csv_agent(
            gcp_model,
            file_path,
            verbose=True,
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            handle_parsing_errors=True,
            #return_intermediate_steps=False,
        )

        # Properly format the user's input and wrap it with the required "input" key
        tool_input = {
            "input": {
                "name": "python",
                "arguments": user_message
            }
        }
        response = agent.run(tool_input, callbacks=[callback]) #.run
        return response
    except Exception as e:
        print(f"Error: {e}")
        return None



### VERSION 1 ####
def gcp_response_v1(prompt: str, df: pd.DataFrame, model=gcp_model_v1):
    template = f"You are a helpful and experienced data scientist expert in data analytics and statistics that always speak in Spanish.\
                      For the given {df} provide valuable insights to question made by the user:\
                      Question:  {prompt} \
                      Answer: If the prompt is empty, in a polite way say that you are ready to answer questions.\
                      If you cannot find the answer of a given question in the data provided, answer that there is not enough data to answer the question.\
                      "

    response = model.generate_content(template)
    return response.text


def gcp_response(prompt: str, df: pd.DataFrame, model=gcp_model):
    template = """You are a helpful and experienced data scientist expert in data analytics and statistics that always speak in Spanish.\
                  For the given {df} provide valuable insights to question made by the user:\
                  Question:  {question} \
                  Answer: If the prompt is empty, in a polite way say that you are ready to answer questions.\
                  If you cannot find the answer of a given question in the data provided, answer that there is not enough data to answer the question.\
                  """
    chat_prompt = PromptTemplate.from_template(template)

    chain = chat_prompt | model

    response = chain.invoke({"question": prompt, "df": df})
    return response


def openai_response(prompt: str, df: pd.DataFrame, model=openai_model):
    template = (
        "You are a helpful and experienced data scientist expert in data analytics, statistics and python that always speak in Spanish.\
         Given the {df} given by the user, provide valuable insights to questions made by the user.\
         If you cannot find the answer of a given question in the data provided, answer that there is not enough data to answer the question.\
         "
    )
    #para generar codigo en python
    #template = (
    #    "You are a helpful and experienced data analyst. Given the {df} given by the user, generate a python code for the question.\
    #     If you cannot find the answer of a given question in the data provided, answer that there is not enough data to answer the question"
    # )
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    human_template = "{text}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    response = model(chat_prompt.format_prompt(df=df, text=prompt).to_messages())
    return response.content
