import os
from dotenv import load_dotenv
import pandas as pd
import vertexai
import google.generativeai as genai
from langchain_openai import ChatOpenAI
from langchain_google_vertexai import VertexAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain.agents.agent_types import AgentType
from langchain_core.messages import HumanMessage
from PIL import Image

#env
load_dotenv()
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'key.json'
GOOGLE_API_KEY = os.environ['GCP_API_KEY']

# OpenAI Models
openai_model_3 = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo', openai_api_key=OPENAI_API_KEY)
openai_model_4 = ChatOpenAI(temperature=0, model_name='gpt-4-turbo-preview', openai_api_key=OPENAI_API_KEY)
# GCP Model (Gemini Pro) v2
gcp_model = VertexAI(temperature=0, model_name="gemini-pro")
gcp_model_vision = ChatGoogleGenerativeAI(temperature=0, model="gemini-pro-vision", google_api_key=GOOGLE_API_KEY)


def analyze_promo_v2(image_path1,image_path2, model=gcp_model_vision):
    '''' just testing for now : same example from gcp'''

    instructions = "Instructions: Consider the following image that contains fruits:"
    prompt1 = "How much should I pay for the fruits given the following price list?"
    prompt2 = """
    Answer the question through these steps:
    Step 1: Identify what kind of fruits there are in the first image.
    Step 2: Count the quantity of each fruit.
    Step 3: For each grocery in first image, check the price of the grocery in the price list.
    Step 4: Calculate the subtotal price for each type of fruit.
    Step 5: Calculate the total price of fruits using the subtotals.

    Answer and describe the steps taken:
    """

    message = HumanMessage(
        content=[
            {
             "type": "text",
             "text": f"{instructions}",
            },
            {"type": "image_url",
             "image_url": image_path1},
            {"type": "text",
             "text": prompt1},
            {"type": "image_url",
             "image_url": image_path2},
            {"type": "text",
             "text": prompt2}
        ]
    )
    response = model.invoke([message]).content
    return response


def analyze_promo(image_path, model=gcp_model_vision):

    prompt = 'Extract all the relevant data from the the image and return it with a json format. Only use the data from the image. Image:'
    prompt2 = ''

    message = HumanMessage(
        content=[
            {
             "type": "text",
             "text": f"{prompt}",
            },
            {"type": "image_url",
             "image_url": image_path}
        ]
    )
    response = model.invoke([message]).content
    return response

def analyze_image(image_path, model=gcp_model_vision, analyst_type=1):
    assert analyst_type in ([1, 2, 3]), 'analyst_type must be in [1,2,3]'

    if analyst_type:
        prompt = 'Que puedes decir acerca de la imágen? Se específico y detallado. Siempre respondes en español.'

    if analyst_type == 2:
        prompt = 'Haz un análisis del siguiente gráfico o tabla. Actúa como un experto en ciencia de datos. Siempre respondes en español.'

    if analyst_type == 3:
        prompt = 'Extract all the relevant data from the the image and return it with a json format. Only use the data from the image.'

    message = HumanMessage(
        content=[
            {
             "type": "text",
             "text": f"{prompt}",
            },  # You can optionally provide text parts
            {"type": "image_url",
             "image_url": image_path}
        ]
    )
    response = model.invoke([message]).content
    return response


def pandas_agent_func(df, user_message, model='gcp', steps=True): #callback,
    try:
        if model == 'gcp':
            model = gcp_model
            agent = AgentType.ZERO_SHOT_REACT_DESCRIPTION
        else:
            model = openai_model_3
            agent = AgentType.OPENAI_FUNCTIONS

        agent = create_pandas_dataframe_agent(
            model,
            df,
            verbose=True,
            agent_type=agent,
            handle_parsing_errors=True,
            return_intermediate_steps=steps,
        )
        tool_input = {
            "input": {
                "name": "python",
                "arguments": f'{user_message}. Always speak in spanish'
            }
        }
        if steps:
            response = agent(tool_input) #, callbacks=[callback]
            return response

        response = agent.run(tool_input) #, callbacks=[callback]
        return response

    except Exception as e:
        print(f"Error: {e}")
        return None


def format_pricing_table(df):
    df = df.iloc[:, :9]
    df.columns = (df.columns.
                  str.replace(' ', '_').
                  str.lower().
                  str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8'))

    df['sku'] = df['sku'].astype(str)
    df['mas_bajo'] = df['mas_bajo'].apply(lambda row: int(row.replace('$ ', '').replace(',', '')))
    df['mas_alto'] = df['mas_alto'].apply(lambda row: int(row.replace('$ ', '').replace(',', '')))
    df['precio_mercado'] = df['precio_mercado'].apply(lambda row: int(row.replace('$ ', '').replace(',', '')))
    df['precio_de_lista'] = df['precio_de_lista'].apply(lambda row: int(row.replace('$ ', '').replace(',', '')))
    df = df.reset_index(drop=True)
    return df

def format_compete_table(df):
    df.columns = (df.columns.
                  str.replace(' ', '_').
                  str.lower().
                  str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8'))

    df['sku_tienda'] = df['sku_tienda'].astype(str)
    df['fecha'] = pd.to_datetime(df['fecha'])
    #df['precio_normal'] = df['precio_normal'].apply(lambda row: int(row.replace('$ ', '').replace(',', '')))
    #df['precio_final'] = df['precio_final'].apply(lambda row: int(row.replace('$ ', '').replace(',', '')))
    #df['precio_tarjeta'] = df['precio_tarjeta'].apply(lambda row: int(row.replace('$ ', '').replace(',', '')))

    df = df.reset_index(drop=True)
    return df
